# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs.memory import scope_path

from .memory_scope import MemoryScope


class CaseInsensitiveDict(dict):
    # pylint: disable=protected-access

    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(
            self.__class__._k(key), *args, **kwargs
        )

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(
            self.__class__._k(key), *args, **kwargs
        )

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(
            self.__class__._k(key), *args, **kwargs
        )

    def update(self, e=None, **f):
        if e is None:
            e = {}
        super(CaseInsensitiveDict, self).update(self.__class__(e))
        super(CaseInsensitiveDict, self).update(self.__class__(**f))

    def _convert_keys(self):
        for k in list(self.keys()):
            val = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, val)


class TurnMemoryScope(MemoryScope):
    def __init__(self):
        super().__init__(scope_path.TURN, False)

    def get_memory(self, dialog_context: "DialogContext") -> object:
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        turn_value = dialog_context.context.turn_state.get(scope_path.TURN, None)

        if not turn_value:
            turn_value = CaseInsensitiveDict()
            dialog_context.context.turn_state[scope_path.TURN] = turn_value

        return turn_value

    def set_memory(self, dialog_context: "DialogContext", memory: object):
        if not dialog_context:
            raise TypeError(f"Expecting: DialogContext, but received None")

        dialog_context.context.turn_state[scope_path.TURN] = memory
