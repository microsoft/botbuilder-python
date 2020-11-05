# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from traceback import print_tb
from typing import Callable, Collection, Generic, Tuple, Type, TypeVar

from botbuilder.core import ComponentRegistration

from botbuilder.dialogs import DialogContext, DialogsComponentRegistration, ObjectPath
from botbuilder.dialogs.memory.scopes import MemoryScope

from .component_memory_scopes_base import ComponentMemoryScopesBase
from .component_path_resolvers_base import ComponentPathResolversBase
from .dialog_state_manager_configuration import DialogStateManagerConfiguration

T = TypeVar('T')      # Declare type variable

# <summary>
# The DialogStateManager manages memory scopes and pathresolvers
# MemoryScopes are named root level objects, which can exist either in the dialogcontext or off of turn state
# PathResolvers allow for shortcut behavior for mapping things like $foo -> dialog.foo.
# </summary>
class DialogStateManager:

    SEPARATORS = [',', '[']

    # <summary>
    # Initializes a new instance of the <see cref="DialogStateManager"/> class.
    # </summary>
    # <param name="dialog_context">The dialog context for the current turn of the conversation.</param>
    # <param name="configuration">Configuration for the dialog state manager. Default is <c>null</c>.</param>
    def __init__(self, dialog_context: DialogContext, configuration: DialogStateManagerConfiguration = None):
        # <summary>
        # Information for tracking when path was last modified.
        # </summary>
        self.path_tracker = "dialog._tracker.paths"

        self._dialog_context = dialog_context
        self._version: int = None

        ComponentRegistration.add(DialogsComponentRegistration())

        if not dialog_context:
            raise TypeError(f"Expecting: {DialogContext.__name__}, but received None")

        self._configuration = configuration or dialog_context.context.turn_state[DialogStateManagerConfiguration.__name__]
        if not self._configuration:
            self._configuration = DialogStateManagerConfiguration()

            # get all of the component memory scopes
            memory_component: ComponentMemoryScopesBase
            for memory_component in filter(lambda comp: isinstance(comp, ComponentMemoryScopesBase), ComponentRegistration.get_components()):
                for memory_scope in memory_component.get_memory_scopes():
                    self._configuration.memory_scopes.append(memory_scope)

            # get all of the component path resolvers
            path_component: ComponentPathResolversBase
            for path_component in filter(lambda comp: isinstance(comp, ComponentPathResolversBase), ComponentRegistration.get_components()):
                for path_resolver in path_component.get_path_resolvers():
                    self._configuration.path_resolvers.append(path_resolver)

        # cache for any other new dialog_state_manager instances in this turn.
        dialog_context.context.turn_state[self._configuration.__class__.__name__] = self._configuration

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
    def keys(self) -> Collection[str]:
        """
        Gets a Collection containing the keys of the memory scopes
        :return: Keys of the memory scopes.
        """
        return [memory_scope.name for memory_scope in self.configuration.memory_scopes]

    @property
    def values(self) -> Collection[object]:
        """
        Gets a Collection containing the values of the memory scopes.
        :return: Values of the memory scopes.
        """
        return [memory_scope.get_memory(self._dialog_context) for memory_scope in self.configuration.memory_scopes]

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
        return self.get_value(key, lambda: None)

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
        return f"'{path}' does not match memory scopes:[{', '.join((memory_scope.name for memory_scope in self.configuration.memory_scopes))}]"

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

        return next((memory_scope for memory_scope in self.configuration.memory_scopes if memory_scope.name.lower() == name.lower()), None)

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
                remaining_path = path[sep_index + 1:]
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

    def _is_primitive(self, cls: Type) -> bool:
        return cls in (int, float, bool, str, complex, float, list, tuple, range, dict, bytes, bytearray, memoryview, set, frozenset, map)

    def try_get_value(self, path: str, class_type: Type) -> Tuple[bool, object]:
        """
        Get the value from memory using path expression (NOTE: This always returns clone of value).
        :param path:
        :param class_type:
        :return: True if found, false if not and the value.
        """
        if not path:
            raise TypeError(f"Expecting: {str.__name__}, but received None")
        return_value = class_type() if self._is_primitive(class_type) else None
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

        # TODO: HACK to support .First() retrieval on turn.recognized.entities.foo, replace with Expressions once expression ship
        first = ".FIRST()"
        i_first = path.upper().rindex(first)
        if i_first >= 0:
            remaining_path = path[i_first + len(first):]
            path = path[0:i_first]
            success, first_value = self.try_get_first_nested_value(path, self)
            if success:
                if not remaining_path:
                    return True, first_value

                path_value = ObjectPath.try_get_path_value(first_value, remaining_path)
                return bool(path_value), path_value

            return False, return_value

        path_value = ObjectPath.try_get_path_value(self, path)
        return bool(path_value), path_value

    # <summary>
    # Get the value from memory using path expression (NOTE: This always returns clone of value).
    # </summary>
    # <remarks>This always returns a CLONE of the memory, any modifications to the result of this will not be affect memory.</remarks>
    # <typeparam name="T">The value type to return.</typeparam>
    # <param name="pathExpression">Path expression to use.</param>
    # <param name="defaultValue">Function to give default value if there is none (OPTIONAL).</param>
    # <returns>Result or null if the path is not valid.</returns>
    def get_value(self, path_expression: str, default_value: Callable[[],Generic[T]] = None) -> T:
        if (TryGetValue<T>(pathExpression ?? throw new ArgumentNullException(nameof(pathExpression)), out value))
        {
            return value
        }

        return defaultValue != null ? defaultValue() : default
    }

    # <summary>
    # Get a int value from memory using a path expression.
    # </summary>
    # <param name="pathExpression">Path expression.</param>
    # <param name="defaultValue">Default value if the value doesn't exist.</param>
    # <returns>Value or null if path is not valid.</returns>
    int GetIntValue(string pathExpression, int defaultValue = 0)
    {
        if (TryGetValue<int>(pathExpression ?? throw new ArgumentNullException(nameof(pathExpression)), out value))
        {
            return value
        }

        return defaultValue
    }

    # <summary>
    # Get a bool value from memory using a path expression.
    # </summary>
    # <param name="pathExpression">The path expression.</param>
    # <param name="defaultValue">Default value if the value doesn't exist.</param>
    # <returns>Bool or null if path is not valid.</returns>
    bool GetBoolValue(string pathExpression, bool defaultValue = false)
    {
        if (TryGetValue<bool>(pathExpression ?? throw new ArgumentNullException(nameof(pathExpression)), out value))
        {
            return value
        }

        return defaultValue
    }

    # <summary>
    # Get a string value from memory using a path expression.
    # </summary>
    # <param name="pathExpression">The path expression.</param>
    # <param name="defaultValue">Default value if the value doesn't exist.</param>
    # <returns>string or null if path is not valid.</returns>
    string GetStringValue(string pathExpression, string defaultValue = default)
    {
        return GetValue(pathExpression, () => defaultValue)
    }

    # <summary>
    # Set memory to value.
    # </summary>
    # <param name="path">Path to memory.</param>
    # <param name="value">Object to set.</param>
    void SetValue(string path, object value)
    {
        if (value is Task)
        {
            throw new Exception($"{path} = You can't pass an unresolved Task to SetValue")
        }

        if (value != null)
        {
            value = JToken.FromObject(value)
        }

        path = TransformPath(path ?? throw new ArgumentNullException(nameof(path)))
        if (TrackChange(path, value))
        {
            ObjectPath.SetPathValue(this, path, value)
        }

        # Every set will increase version
        _version++
    }

    # <summary>
    # Remove property from memory.
    # </summary>
    # <param name="path">Path to remove the leaf property.</param>
    void RemoveValue(string path)
    {
        path = TransformPath(path ?? throw new ArgumentNullException(nameof(path)))
        if (TrackChange(path, null))
        {
            ObjectPath.RemovePathValue(this, path)
        }
    }

    # <summary>
    # Gets all memoryscopes suitable for logging.
    # </summary>
    # <returns>object which represents all memory scopes.</returns>
    JObject GetMemorySnapshot()
    {
        result = new JObject()

        foreach (scope in Configuration.MemoryScopes.Where(ms => ms.IncludeInSnapshot))
        {
            memory = scope.GetMemory(_dialogContext)
            if (memory != null)
            {
                result[scope.Name] = JToken.FromObject(memory)
            }
        }

        return result
    }

    # <summary>
    # Load all of the scopes.
    # </summary>
    # <param name="cancellationToken">cancellationToken.</param>
    # <returns>Task.</returns>
    async Task LoadAllScopesAsync(CancellationToken cancellationToken = default)
    {
        foreach (scope in Configuration.MemoryScopes)
        {
            await scope.LoadAsync(_dialogContext, cancellationToken: cancellationToken).ConfigureAwait(false)
        }
    }

    # <summary>
    # Save all changes for all scopes.
    # </summary>
    # <param name="cancellationToken">cancellationToken.</param>
    # <returns>Task.</returns>
    async Task SaveAllChangesAsync(CancellationToken cancellationToken = default)
    {
        foreach (scope in Configuration.MemoryScopes)
        {
            await scope.SaveChangesAsync(_dialogContext, cancellationToken: cancellationToken).ConfigureAwait(false)
        }
    }

    # <summary>
    # Delete the memory for a scope.
    # </summary>
    # <param name="name">name of the scope.</param>
    # <param name="cancellationToken">cancellationToken.</param>
    # <returns>Task.</returns>
    async Task DeleteScopesMemoryAsync(string name, CancellationToken cancellationToken = default)
    {
        name = name.ToUpperInvariant()
        scope = Configuration.MemoryScopes.SingleOrDefault(s => s.Name.ToUpperInvariant() == name)
        if (scope != null)
        {
            await scope.DeleteAsync(_dialogContext, cancellationToken).ConfigureAwait(false)
        }
    }

    # <summary>
    # Adds an element to the dialog state manager.
    # </summary>
    # <param name="key">Key of the element to add.</param>
    # <param name="value">Value of the element to add.</param>
    void Add(string key, object value)
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Determines whether the dialog state manager contains an element with the specified key.
    # </summary>
    # <param name="key">The key to locate in the dialog state manager.</param>
    # <returns><c>true</c> if the dialog state manager contains an element with
    # the key otherwise, <c>false</c>.</returns>
    bool ContainsKey(string key)
    {
        return Configuration.MemoryScopes.Any(ms => ms.Name.ToUpperInvariant() == key.ToUpperInvariant())
    }

    # <summary>
    # Removes the element with the specified key from the dialog state manager.
    # </summary>
    # <param name="key">The key of the element to remove.</param>
    # <returns><c>true</c> if the element is succesfully removed otherwise, false.</returns>
    # <remarks>This method is not supported.</remarks>
    bool Remove(string key)
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Gets the value associated with the specified key.
    # </summary>
    # <param name="key">The key whose value to get.</param>
    # <param name="value">When this method returns, the value associated with the specified key, if the
    # key is found otherwise, the default value for the type of the value parameter.
    # This parameter is passed uninitialized.</param>
    # <returns><c>true</c> if the dialog state manager contains an element with the specified key
    # otherwise, <c>false</c>.</returns>
    bool TryGetValue(string key, out object value)
    {
        return TryGetValue<object>(key, out value)
    }

    # <summary>
    # Adds an item to the dialog state manager.
    # </summary>
    # <param name="item">The <see cref="KeyValuePair{TKey, TValue}"/> with the key and object of
    # the item to add.</param>
    # <remarks>This method is not supported.</remarks>
    void Add(KeyValuePair<string, object> item)
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Removes all items from the dialog state manager.
    # </summary>
    # <remarks>This method is not supported.</remarks>
    void Clear()
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Determines whether the dialog state manager contains a specific value.
    # </summary>
    # <param name="item">The <see cref="KeyValuePair{TKey, TValue}"/> of the item to locate.</param>
    # <returns><c>true</c> if item is found in the dialog state manager otherwise,
    # <c>false</c>.</returns>
    # <remarks>This method is not supported.</remarks>
    bool Contains(KeyValuePair<string, object> item)
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Copies the elements of the dialog state manager to an array starting at a particular index.
    # </summary>
    # <param name="array">The one-dimensional array that is the destination of the elements copied
    # from the dialog state manager. The array must have zero-based indexing.</param>
    # <param name="arrayIndex">The zero-based index in array at which copying begins.</param>
    void CopyTo(KeyValuePair<string, object>[] array, int arrayIndex)
    {
        foreach (ms in Configuration.MemoryScopes)
        {
            array[arrayIndex++] = new KeyValuePair<string, object>(ms.Name, ms.GetMemory(_dialogContext))
        }
    }

    # <summary>
    # Removes the first occurrence of a specific object from the dialog state manager.
    # </summary>
    # <param name="item">The object to remove from the dialog state manager.</param>
    # <returns><c>true</c> if the item was successfully removed from the dialog state manager
    # otherwise, <c>false</c>.</returns>
    # <remarks>This method is not supported.</remarks>
    bool Remove(KeyValuePair<string, object> item)
    {
        throw new NotSupportedException()
    }

    # <summary>
    # Returns an enumerator that iterates through the collection.
    # </summary>
    # <returns>An enumerator that can be used to iterate through the collection.</returns>
    IEnumerator<KeyValuePair<string, object>> GetEnumerator()
    {
        foreach (ms in Configuration.MemoryScopes)
        {
            yield return new KeyValuePair<string, object>(ms.Name, ms.GetMemory(_dialogContext))
        }
    }

    # <summary>
    # Track when specific paths are changed.
    # </summary>
    # <param name="paths">Paths to track.</param>
    # <returns>Normalized paths to pass to <see cref="AnyPathChanged"/>.</returns>
    List<string> TrackPaths(IEnumerable<string> paths)
    {
        allPaths = new List<string>()
        foreach (path in paths)
        {
            tpath = TransformPath(path)

            # Track any path that resolves to a constant path
            if (ObjectPath.TryResolvePath(this, tpath, out segments))
            {
                npath = string.Join("_", segments)
                SetValue(PathTracker + "." + npath, 0)
                allPaths.Add(npath)
            }
        }

        return allPaths
    }

    # <summary>
    # Check to see if any path has changed since watermark.
    # </summary>
    # <param name="counter">Time counter to compare to.</param>
    # <param name="paths">Paths from <see cref="TrackPaths"/> to check.</param>
    # <returns>True if any path has changed since counter.</returns>
    bool AnyPathChanged(uint counter, IEnumerable<string> paths)
    {
        found = false
        if (paths != null)
        {
            foreach (path in paths)
            {
                if (GetValue<uint>(PathTracker + "." + path) > counter)
                {
                    found = true
                    break
                }
            }
        }

        return found
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        foreach (ms in Configuration.MemoryScopes)
        {
            yield return new KeyValuePair<string, object>(ms.Name, ms.GetMemory(_dialogContext))
        }
    }

    static bool TryGetFirstNestedValue<T>(ref T value, ref string remainingPath, object memory)
    {
        if (ObjectPath.TryGetPathValue < JArray > (memory, remaining_path, out array))
        {
            if (array != null && array.Count > 0)
            {
                if (array[0] is JArray first)
                {
                    if (first.Count > 0)
                    {
                        second = first[0]
                        value = ObjectPath.MapValueTo<T>(second)
                        return true
                    }

                    return false
                }

                value = ObjectPath.MapValueTo<T>(array[0])
                return true
            }
        }

        return false
    }

    string GetBadScopeMessage(string path)
    {
        return $"'{path}' does not match memory scopes:[{string.Join(",", Configuration.MemoryScopes.Select(ms => ms.Name))}]"
    }

    bool TrackChange(string path, object value)
    {
        hasPath = false
        if (ObjectPath.TryResolvePath(this, path, out segments))
        {
            root = segments.Count > 1 ? segments[1] as string : string.Empty

            # Skip _* as first scope, i.e. _adaptive, _tracker, ...
            if (!root.StartsWith("_", StringComparison.Ordinal))
            {
                # Convert to a simple path with _ between segments
                pathName = string.Join("_", segments)
                trackedPath = $"{PathTracker}.{pathName}"
                uint? counter = null

                void Update()
                {
                    if (TryGetValue<uint>(trackedPath, out lastChanged))
                    {
                        if (!counter.HasValue)
                        {
                            counter = GetValue<uint>(DialogPath.EventCounter)
                        }

                        SetValue(trackedPath, counter.Value)
                    }
                }

                Update()
                if (value is object obj)
                {
                    # For an object we need to see if any children path are being tracked
                    void CheckChildren(string property, object instance)
                    {
                        # Add new child segment
                        trackedPath += "_" + property.ToLowerInvariant()
                        Update()
                        if (instance is object child)
                        {
                            ObjectPath.ForEachProperty(child, CheckChildren)
                        }

                        # Remove added child segment
                        trackedPath = trackedPath.Substring(0, trackedPath.LastIndexOf('_'))
                    }

                    ObjectPath.ForEachProperty(obj, CheckChildren)
                }
            }

            hasPath = true
        }

        return hasPath
    }
}
