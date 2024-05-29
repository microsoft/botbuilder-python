# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import builtins

from inspect import isawaitable
from traceback import print_tb
from typing import (
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Tuple,
    Type,
    TypeVar,
)

from botbuilder.core import ComponentRegistration

from botbuilder.dialogs.memory.scopes import MemoryScope

from .component_memory_scopes_base import ComponentMemoryScopesBase
from .component_path_resolvers_base import ComponentPathResolversBase
from .dialog_path import DialogPath
from .dialog_state_manager_configuration import DialogStateManagerConfiguration

# Declare type variable
T = TypeVar("T")  # pylint: disable=invalid-name

BUILTIN_TYPES = list(filter(lambda x: not x.startswith("_"), dir(builtins)))


# <summary>
# The DialogStateManager manages memory scopes and pathresolvers
# MemoryScopes are named root level objects, which can exist either in the dialogcontext or off of turn state
# PathResolvers allow for shortcut behavior for mapping things like $foo -> dialog.foo.
# </summary>
class DialogStateManager:
    SEPARATORS = [",", "["]

    def __init__(
        self,
        dialog_context: "DialogContext",
        configuration: DialogStateManagerConfiguration = None,
    ):
        """
        Initializes a new instance of the DialogStateManager class.
        :param dialog_context: The dialog context for the current turn of the conversation.
        :param configuration: Configuration for the dialog state manager. Default is None.
        """
        # pylint: disable=import-outside-toplevel
        # These modules are imported at static level to avoid circular dependency problems
        from botbuilder.dialogs import (
            DialogsComponentRegistration,
            ObjectPath,
        )

        self._object_path_cls = ObjectPath
        self._dialog_component_registration_cls = DialogsComponentRegistration

        # Information for tracking when path was last modified.
        self.path_tracker = "dialog._tracker.paths"

        self._dialog_context = dialog_context
        self._version: int = 0

        ComponentRegistration.add(self._dialog_component_registration_cls())

        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        self._configuration = configuration or dialog_context.context.turn_state.get(
            DialogStateManagerConfiguration.__name__, None
        )
        if not self._configuration:
            self._configuration = DialogStateManagerConfiguration()

            # get all of the component memory scopes
            memory_component: ComponentMemoryScopesBase
            for memory_component in filter(
                lambda comp: isinstance(comp, ComponentMemoryScopesBase),
                ComponentRegistration.get_components(),
            ):
                for memory_scope in memory_component.get_memory_scopes():
                    self._configuration.memory_scopes.append(memory_scope)

            # get all of the component path resolvers
            path_component: ComponentPathResolversBase
            for path_component in filter(
                lambda comp: isinstance(comp, ComponentPathResolversBase),
                ComponentRegistration.get_components(),
            ):
                for path_resolver in path_component.get_path_resolvers():
                    self._configuration.path_resolvers.append(path_resolver)

        # cache for any other new dialog_state_manager instances in this turn.
        dialog_context.context.turn_state[self._configuration.__class__.__name__] = (
            self._configuration
        )

    def __len__(self) -> int:
        """
        Gets the number of memory scopes in the dialog state manager.
        :return: Number of memory scopes in the configuration.
        """
        return len(self._configuration.memory_scopes)

    @property
    def configuration(self) -> DialogStateManagerConfiguration:
        """
        Gets or sets the configured path resolvers and memory scopes for the dialog state manager.
        :return: The configuration object.
        """
        return self._configuration

    @property
    def keys(self) -> Iterable[str]:
        """
        Gets a Iterable containing the keys of the memory scopes
        :return: Keys of the memory scopes.
        """
        return [memory_scope.name for memory_scope in self.configuration.memory_scopes]

    @property
    def values(self) -> Iterable[object]:
        """
        Gets a Iterable containing the values of the memory scopes.
        :return: Values of the memory scopes.
        """
        return [
            memory_scope.get_memory(self._dialog_context)
            for memory_scope in self.configuration.memory_scopes
        ]

    # <summary>
    # Gets a value indicating whether the dialog state manager is read-only.
    # </summary>
    # <value><c>true</c>.</value>
    @property
    def is_read_only(self) -> bool:
        """
        Gets a value indicating whether the dialog state manager is read-only.
        :return: True.
        """
        return True

    # <summary>
    # Gets or sets the elements with the specified key.
    # </summary>
    # <param name="key">Key to get or set the element.</param>
    # <returns>The element with the specified key.</returns>
    def __getitem__(self, key):
        """
        :param key:
        :return The value stored at key's position:
        """
        return self.get_value(object, key, default_value=lambda: None)

    def __setitem__(self, key, value):
        if self._index_of_any(key, self.SEPARATORS) == -1:
            # Root is handled by SetMemory rather than SetValue
            scope = self.get_memory_scope(key)
            if not scope:
                raise IndexError(self._get_bad_scope_message(key))
            # TODO: C# transforms value to JToken
            scope.set_memory(self._dialog_context, value)
        else:
            self.set_value(key, value)

    def _get_bad_scope_message(self, path: str) -> str:
        return (
            f"'{path}' does not match memory scopes:["
            f"{', '.join((memory_scope.name for memory_scope in self.configuration.memory_scopes))}]"
        )

    @staticmethod
    def _index_of_any(string: str, elements_to_search_for) -> int:
        for element in elements_to_search_for:
            index = string.find(element)
            if index != -1:
                return index

        return -1

    def get_memory_scope(self, name: str) -> MemoryScope:
        """
        Get MemoryScope by name.
        :param name:
        :return: A memory scope.
        """
        if not name:
            raise TypeError(f"Expecting: {str.__name__}, but received None")

        return next(
            (
                memory_scope
                for memory_scope in self.configuration.memory_scopes
                if memory_scope.name.lower() == name.lower()
            ),
            None,
        )

    def version(self) -> str:
        """
        Version help caller to identify the updates and decide cache or not.
        :return: Current version.
        """
        return str(self._version)

    def resolve_memory_scope(self, path: str) -> Tuple[MemoryScope, str]:
        """
        Will find the MemoryScope for and return the remaining path.
        :param path:
        :return: The memory scope and remaining subpath in scope.
        """
        scope = path
        sep_index = -1
        dot = path.find(".")
        open_square_bracket = path.find("[")

        if dot > 0 and open_square_bracket > 0:
            sep_index = min(dot, open_square_bracket)

        elif dot > 0:
            sep_index = dot

        elif open_square_bracket > 0:
            sep_index = open_square_bracket

        if sep_index > 0:
            scope = path[0:sep_index]
            memory_scope = self.get_memory_scope(scope)
            if memory_scope:
                remaining_path = path[sep_index + 1 :]
                return memory_scope, remaining_path

        memory_scope = self.get_memory_scope(scope)
        if not scope:
            raise IndexError(self._get_bad_scope_message(scope))
        return memory_scope, ""

    def transform_path(self, path: str) -> str:
        """
        Transform the path using the registered PathTransformers.
        :param path: Path to transform.
        :return: The transformed path.
        """
        for path_resolver in self.configuration.path_resolvers:
            path = path_resolver.transform_path(path)

        return path

    @staticmethod
    def _is_primitive(type_to_check: Type) -> bool:
        return type_to_check.__name__ in BUILTIN_TYPES

    def try_get_value(
        self, path: str, class_type: Type = object
    ) -> Tuple[bool, object]:
        """
        Get the value from memory using path expression (NOTE: This always returns clone of value).
        :param class_type: The value type to return.
        :param path: Path expression to use.
        :return: True if found, false if not and the value.
        """
        if not path:
            raise TypeError(f"Expecting: {str.__name__}, but received None")
        return_value = (
            class_type() if DialogStateManager._is_primitive(class_type) else None
        )
        path = self.transform_path(path)

        try:
            memory_scope, remaining_path = self.resolve_memory_scope(path)
        except Exception as error:
            print_tb(error.__traceback__)
            return False, return_value

        if not memory_scope:
            return False, return_value

        if not remaining_path:
            memory = memory_scope.get_memory(self._dialog_context)
            if not memory:
                return False, return_value

            return True, memory

        # TODO: HACK to support .First() retrieval on turn.recognized.entities.foo, replace with Expressions once
        #  expressions ship
        first = ".FIRST()"
        try:
            i_first = path.upper().rindex(first)
        except ValueError:
            i_first = -1
        if i_first >= 0:
            remaining_path = path[i_first + len(first) :]
            path = path[0:i_first]
            success, first_value = self._try_get_first_nested_value(path, self)
            if success:
                if not remaining_path:
                    return True, first_value

                path_value = self._object_path_cls.try_get_path_value(
                    first_value, remaining_path
                )
                return bool(path_value), path_value

            return False, return_value

        path_value = self._object_path_cls.try_get_path_value(self, path)
        return bool(path_value), path_value

    def get_value(
        self,
        class_type: Type,
        path_expression: str,
        default_value: Callable[[], T] = None,
    ) -> T:
        """
        Get the value from memory using path expression (NOTE: This always returns clone of value).
        :param class_type: The value type to return.
        :param path_expression: Path expression to use.
        :param default_value: Function to give default value if there is none (OPTIONAL).
        :return: Result or null if the path is not valid.
        """
        if not path_expression:
            raise TypeError(f"Expecting: {str.__name__}, but received None")

        success, value = self.try_get_value(path_expression, class_type)
        if success:
            return value

        return default_value() if default_value else None

    def get_int_value(self, path_expression: str, default_value: int = 0) -> int:
        """
        Get an int value from memory using a path expression.
        :param path_expression: Path expression to use.
        :param default_value: Default value if there is none (OPTIONAL).
        :return:
        """
        if not path_expression:
            raise TypeError(f"Expecting: {str.__name__}, but received None")
        success, value = self.try_get_value(path_expression, int)
        if success:
            return value

        return default_value

    def get_bool_value(self, path_expression: str, default_value: bool = False) -> bool:
        """
        Get a bool value from memory using a path expression.
        :param path_expression: Path expression to use.
        :param default_value: Default value if there is none (OPTIONAL).
        :return:
        """
        if not path_expression:
            raise TypeError(f"Expecting: {str.__name__}, but received None")
        success, value = self.try_get_value(path_expression, bool)
        if success:
            return value

        return default_value

    def get_string_value(self, path_expression: str, default_value: str = "") -> str:
        """
        Get a string value from memory using a path expression.
        :param path_expression: Path expression to use.
        :param default_value: Default value if there is none (OPTIONAL).
        :return:
        """
        if not path_expression:
            raise TypeError(f"Expecting: {str.__name__}, but received None")
        success, value = self.try_get_value(path_expression, str)
        if success:
            return value

        return default_value

    def set_value(self, path: str, value: object):
        """
        Set memory to value.
        :param path: Path to memory.
        :param value: Object to set.
        :return:
        """
        if isawaitable(value):
            raise Exception(f"{path} = You can't pass an awaitable to set_value")

        if not path:
            raise TypeError(f"Expecting: {str.__name__}, but received None")

        path = self.transform_path(path)
        if self._track_change(path, value):
            self._object_path_cls.set_path_value(self, path, value)

        # Every set will increase version
        self._version += 1

    def remove_value(self, path: str):
        """
        Set memory to value.
        :param path: Path to memory.
        :param value: Object to set.
        :return:
        """
        if not path:
            raise TypeError(f"Expecting: {str.__name__}, but received None")

        path = self.transform_path(path)
        if self._track_change(path, None):
            self._object_path_cls.remove_path_value(self, path)

    def get_memory_snapshot(self) -> Dict[str, object]:
        """
        Gets all memoryscopes suitable for logging.
        :return: object which represents all memory scopes.
        """
        result = {}

        for scope in [
            ms for ms in self.configuration.memory_scopes if ms.include_in_snapshot
        ]:
            memory = scope.get_memory(self._dialog_context)
            if memory:
                result[scope.name] = memory

        return result

    async def load_all_scopes(self):
        """
        Load all of the scopes.
        :return:
        """
        for scope in self.configuration.memory_scopes:
            await scope.load(self._dialog_context)

    async def save_all_changes(self):
        """
        Save all changes for all scopes.
        :return:
        """
        for scope in self.configuration.memory_scopes:
            await scope.save_changes(self._dialog_context)

    async def delete_scopes_memory_async(self, name: str):
        """
        Delete the memory for a scope.
        :param name: name of the scope.
        :return:
        """
        name = name.upper()
        scope_list = [
            ms for ms in self.configuration.memory_scopes if ms.name.upper == name
        ]
        if len(scope_list) > 1:
            raise RuntimeError(f"More than 1 scopes found with the name '{name}'")
        scope = scope_list[0] if scope_list else None
        if scope:
            await scope.delete(self._dialog_context)

    def add(self, key: str, value: object):
        """
        Adds an element to the dialog state manager.
        :param key: Key of the element to add.
        :param value: Value of the element to add.
        :return:
        """
        raise RuntimeError("Not supported")

    def contains_key(self, key: str) -> bool:
        """
        Determines whether the dialog state manager contains an element with the specified key.
        :param key: The key to locate in the dialog state manager.
        :return: True if the dialog state manager contains an element with the key otherwise, False.
        """
        scopes_with_key = [
            ms
            for ms in self.configuration.memory_scopes
            if ms.name.upper == key.upper()
        ]
        return bool(scopes_with_key)

    def remove(self, key: str):
        """
        Removes the element with the specified key from the dialog state manager.
        :param key: Key of the element to remove.
        :return:
        """
        raise RuntimeError("Not supported")

    # <summary>
    # Removes all items from the dialog state manager.
    # </summary>
    # <remarks>This method is not supported.</remarks>
    def clear(self, key: str):
        """
        Removes all items from the dialog state manager.
        :param key: Key of the element to remove.
        :return:
        """
        raise RuntimeError("Not supported")

    def contains(self, item: Tuple[str, object]) -> bool:
        """
        Determines whether the dialog state manager contains a specific value (should use __contains__).
        :param item: The tuple of the item to locate.
        :return bool: True if item is found in the dialog state manager otherwise, False
        """
        raise RuntimeError("Not supported")

    def __contains__(self, item: Tuple[str, object]) -> bool:
        """
        Determines whether the dialog state manager contains a specific value.
        :param item: The tuple of the item to locate.
        :return bool: True if item is found in the dialog state manager otherwise, False
        """
        raise RuntimeError("Not supported")

    def copy_to(self, array: List[Tuple[str, object]], array_index: int):
        """
        Copies the elements of the dialog state manager to an array starting at a particular index.
        :param array: The one-dimensional array that is the destination of the elements copied
         from the dialog state manager. The array must have zero-based indexing.
        :param array_index:
        :return:
        """
        for memory_scope in self.configuration.memory_scopes:
            array[array_index] = (
                memory_scope.name,
                memory_scope.get_memory(self._dialog_context),
            )
            array_index += 1

    def remove_item(self, item: Tuple[str, object]) -> bool:
        """
        Determines whether the dialog state manager contains a specific value (should use __contains__).
        :param item: The tuple of the item to locate.
        :return bool: True if item is found in the dialog state manager otherwise, False
        """
        raise RuntimeError("Not supported")

    # <summary>
    # Returns an enumerator that iterates through the collection.
    # </summary>
    # <returns>An enumerator that can be used to iterate through the collection.</returns>
    def get_enumerator(self) -> Iterator[Tuple[str, object]]:
        """
        Returns an enumerator that iterates through the collection.
        :return: An enumerator that can be used to iterate through the collection.
        """
        for memory_scope in self.configuration.memory_scopes:
            yield (memory_scope.name, memory_scope.get_memory(self._dialog_context))

    def track_paths(self, paths: Iterable[str]) -> List[str]:
        """
        Track when specific paths are changed.
        :param paths: Paths to track.
        :return: Normalized paths to pass to any_path_changed.
        """
        all_paths = []
        for path in paths:
            t_path = self.transform_path(path)

            # Track any path that resolves to a constant path
            segments = self._object_path_cls.try_resolve_path(self, t_path)
            if segments:
                n_path = "_".join(segments)
                self.set_value(self.path_tracker + "." + n_path, 0)
                all_paths.append(n_path)

        return all_paths

    def any_path_changed(self, counter: int, paths: Iterable[str]) -> bool:
        """
        Check to see if any path has changed since watermark.
        :param counter: Time counter to compare to.
        :param paths: Paths from track_paths to check.
        :return: True if any path has changed since counter.
        """
        found = False
        if paths:
            for path in paths:
                if self.get_value(int, self.path_tracker + "." + path) > counter:
                    found = True
                    break

        return found

    def __iter__(self):
        for memory_scope in self.configuration.memory_scopes:
            yield (memory_scope.name, memory_scope.get_memory(self._dialog_context))

    @staticmethod
    def _try_get_first_nested_value(
        remaining_path: str, memory: object
    ) -> Tuple[bool, object]:
        # These modules are imported at static level to avoid circular dependency problems
        # pylint: disable=import-outside-toplevel

        from botbuilder.dialogs import ObjectPath

        array = ObjectPath.try_get_path_value(memory, remaining_path)
        if array:
            if isinstance(array[0], list):
                first = array[0]
                if first:
                    second = first[0]
                    return True, second

                return False, None

            return True, array[0]

        return False, None

    def _track_change(self, path: str, value: object) -> bool:
        has_path = False
        segments = self._object_path_cls.try_resolve_path(self, path)
        if segments:
            root = segments[1] if len(segments) > 1 else ""

            # Skip _* as first scope, i.e. _adaptive, _tracker, ...
            if not root.startswith("_"):
                # Convert to a simple path with _ between segments
                path_name = "_".join(segments)
                tracked_path = f"{self.path_tracker}.{path_name}"
                counter = None

                def update():
                    nonlocal counter
                    last_changed = self.try_get_value(tracked_path, int)
                    if last_changed:
                        if counter is not None:
                            counter = self.get_value(int, DialogPath.EVENT_COUNTER)

                        self.set_value(tracked_path, counter)

                update()
                if not self._is_primitive(type(value)):
                    # For an object we need to see if any children path are being tracked
                    def check_children(property: str, instance: object):
                        nonlocal tracked_path
                        # Add new child segment
                        tracked_path += "_" + property.lower()
                        update()
                        if not self._is_primitive(type(instance)):
                            self._object_path_cls.for_each_property(
                                property, check_children
                            )

                        # Remove added child segment
                        tracked_path = tracked_path.Substring(
                            0, tracked_path.LastIndexOf("_")
                        )

                    self._object_path_cls.for_each_property(value, check_children)

            has_path = True

        return has_path
