# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import copy
from typing import Union, Callable


class ObjectPath:
    """
    Helper methods for working with json objects.
    """

    @staticmethod
    def assign(start_object, overlay_object, default: Union[Callable, object] = None):
        """
        Creates a new object by overlaying values in start_object with non-null values from overlay_object.

        :param start_object: dict or typed object, the target object to set values on
        :param overlay_object: dict or typed object, the item to overlay values form
        :param default: Provides a default object if both source and overlay are None
        :return: A copy of start_object, with values from overlay_object
        """
        if start_object and overlay_object:
            merged = copy.deepcopy(start_object)

            def merge(target: dict, source: dict):
                key_set = set(target).union(set(source))

                for key in key_set:
                    target_value = target.get(key)
                    source_value = source.get(key)

                    # skip empty overlay items
                    if source_value:
                        if isinstance(source_value, dict):
                            # merge dictionaries
                            if not target_value:
                                target[key] = copy.deepcopy(source_value)
                            else:
                                merge(target_value, source_value)
                        elif not hasattr(source_value, "__dict__"):
                            # simple type.  just copy it.
                            target[key] = copy.copy(source_value)
                        elif not target_value:
                            # the target doesn't have the value, but
                            # the overlay does.  just copy it.
                            target[key] = copy.deepcopy(source_value)
                        else:
                            # recursive class copy
                            merge(target_value.__dict__, source_value.__dict__)

            target_dict = merged if isinstance(merged, dict) else merged.__dict__
            overlay_dict = (
                overlay_object
                if isinstance(overlay_object, dict)
                else overlay_object.__dict__
            )
            merge(target_dict, overlay_dict)

            return merged

        if overlay_object:
            return copy.deepcopy(overlay_object)

        if start_object:
            return start_object
        if default:
            return default() if callable(default) else copy.deepcopy(default)
        return None

    @staticmethod
    def set_path_value(obj, path: str, value: object):
        """
        Given an object evaluate a path to set the value.
        """

        segments = ObjectPath.try_resolve_path(obj, path)
        if not segments:
            return

        current = obj
        for i in range(len(segments) - 1):
            segment = segments[i]
            if ObjectPath.is_int(segment):
                index = int(segment)
                next_obj = current[index]
                if not next_obj and len(current) <= index:
                    # Expand list to index
                    current += [None] * ((index + 1) - len(current))
                    next_obj = current[index]
            else:
                next_obj = ObjectPath.__get_object_property(current, segment)
                if not next_obj:
                    # Create object or list based on next segment
                    next_segment = segments[i + 1]
                    if not ObjectPath.is_int(next_segment):
                        ObjectPath.__set_object_segment(current, segment, {})
                    else:
                        ObjectPath.__set_object_segment(current, segment, [])

                    next_obj = ObjectPath.__get_object_property(current, segment)

            current = next_obj

        last_segment = segments[-1]
        ObjectPath.__set_object_segment(current, last_segment, value)

    @staticmethod
    def get_path_value(
        obj, path: str, default: Union[Callable, object] = None
    ) -> object:
        """
        Get the value for a path relative to an object.
        """

        value = ObjectPath.try_get_path_value(obj, path)
        if value:
            return value

        if default is None:
            raise KeyError(f"Key {path} not found")
        return default() if callable(default) else copy.deepcopy(default)

    @staticmethod
    def has_value(obj, path: str) -> bool:
        """
        Does an object have a subpath.
        """
        return ObjectPath.try_get_path_value(obj, path) is not None

    @staticmethod
    def remove_path_value(obj, path: str):
        """
        Remove path from object.
        """

        segments = ObjectPath.try_resolve_path(obj, path)
        if not segments:
            return

        current = obj
        for i in range(len(segments) - 1):
            segment = segments[i]
            current = ObjectPath.__resolve_segment(current, segment)
            if not current:
                return

        if current:
            last_segment = segments[-1]
            if ObjectPath.is_int(last_segment):
                current[int(last_segment)] = None
            else:
                current.pop(last_segment)

    @staticmethod
    def try_get_path_value(obj, path: str) -> object:
        """
        Get the value for a path relative to an object.
        """

        if not obj:
            return None

        if path is None:
            return None

        if not path:
            return obj

        segments = ObjectPath.try_resolve_path(obj, path)
        if not segments:
            return None

        result = ObjectPath.__resolve_segments(obj, segments)
        if not result:
            return None

        return result

    @staticmethod
    def __set_object_segment(obj, segment, value):
        val = ObjectPath.__get_normalized_value(value)

        if ObjectPath.is_int(segment):
            # the target is an list
            index = int(segment)

            # size the list if needed
            obj += [None] * ((index + 1) - len(obj))

            obj[index] = val
            return

        # the target is a dictionary
        obj[segment] = val

    @staticmethod
    def __get_normalized_value(value):
        return value

    @staticmethod
    def try_resolve_path(obj, property_path: str, evaluate: bool = False) -> []:
        so_far = []
        first = property_path[0] if property_path else " "
        if first in ("'", '"'):
            if not property_path.endswith(first):
                return None

            so_far.append(property_path[1 : len(property_path) - 2])
        elif ObjectPath.is_int(property_path):
            so_far.append(int(property_path))
        else:
            start = 0
            i = 0

            def emit():
                nonlocal start, i
                segment = property_path[start:i]
                if segment:
                    so_far.append(segment)
                start = i + 1

            while i < len(property_path):
                char = property_path[i]
                if char in (".", "["):
                    emit()

                if char == "[":
                    nesting = 1
                    i += 1
                    while i < len(property_path):
                        char = property_path[i]
                        if char == "[":
                            nesting += 1
                        elif char == "]":
                            nesting -= 1
                            if nesting == 0:
                                break
                        i += 1

                    if nesting > 0:
                        return None

                    expr = property_path[start:i]
                    start = i + 1
                    indexer = ObjectPath.try_resolve_path(obj, expr, True)
                    if not indexer:
                        return None

                    result = indexer[0]
                    if ObjectPath.is_int(result):
                        so_far.append(int(result))
                    else:
                        so_far.append(result)

                i += 1

            emit()

            if evaluate:
                result = ObjectPath.__resolve_segments(obj, so_far)
                if not result:
                    return None

                so_far.clear()
                so_far.append(result)

        return so_far

    @staticmethod
    def for_each_property(obj: object, action: Callable[[str, object], None]):
        if isinstance(obj, dict):
            for key, value in obj.items():
                action(key, value)
        elif hasattr(obj, "__dict__"):
            for key, value in vars(obj).items():
                action(key, value)

    @staticmethod
    def __resolve_segments(current, segments: []) -> object:
        result = current

        for segment in segments:
            result = ObjectPath.__resolve_segment(result, segment)
            if not result:
                return None

        return result

    @staticmethod
    def __resolve_segment(current, segment) -> object:
        if current:
            if ObjectPath.is_int(segment):
                current = current[int(segment)]
            else:
                current = ObjectPath.__get_object_property(current, segment)

        return current

    @staticmethod
    def __get_object_property(obj, property_name: str):
        # doing a case insensitive search
        property_name_lower = property_name.lower()
        matching = [obj[key] for key in obj if key.lower() == property_name_lower]
        return matching[0] if matching else None

    @staticmethod
    def is_int(value: str) -> bool:
        try:
            int(value)
            return True
        except ValueError:
            return False
