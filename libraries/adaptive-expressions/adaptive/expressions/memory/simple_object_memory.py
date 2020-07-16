import re
import json

from ..memory_interface import MemoryInterface
from ..extensions import Extensions
from ..function_utils import FunctionUtils


class SimpleObjectMemory(MemoryInterface):
    memory = None

    def __init__(self, memory: object):
        self.memory = memory

    @staticmethod
    def wrap(obj: object) -> MemoryInterface:
        if Extensions.is_memeory_interface(obj):
            return obj

        return SimpleObjectMemory(obj)

    def get_value(self, path: str) -> object:
        if self.memory is None or len(path) == 0:
            return None

        parts = re.findall(r"\[([^[\]]*)\]", path)
        parts = list(
            map(
                lambda x: x[1:-1]
                if x.startswith('"')
                and x.endswith('"')
                or x.startswith("'")
                and x.endswith("'")
                else x,
                parts,
            )
        )
        parts = list(filter(lambda x: (x is not None and x), parts))

        value = None
        cur_scope = self.memory

        for part in parts:
            error: str
            is_int = self.is_int(part)
            if is_int and isinstance(cur_scope, list):
                idx = int(part)
                value, error = FunctionUtils.access_index(cur_scope, idx)
            else:
                value, error = FunctionUtils.access_property(cur_scope, part)

            if error is not None:
                return None

            cur_scope = value

        return value

    def set_value(self, path: str, input: object):
        if self.memory is None:
            return

        parts = re.findall(r"\[([^[\]]*)\]", path)
        parts = list(
            map(
                lambda x: x[1:-1]
                if x.startswith('"')
                and x.endswith('"')
                or x.startswith("'")
                and x.endswith("'")
                else x,
                parts,
            )
        )
        parts = list(filter(lambda x: (x is not None and x), parts))

        cur_scope = self.memory
        error = None

        for i in range(len(parts) - 1):
            is_int = self.is_int(parts[i])
            if is_int and isinstance(cur_scope, list):
                idx = int(parts[i])
                value, error = FunctionUtils.access_index(cur_scope, idx)
            else:
                value, error = FunctionUtils.access_property(cur_scope, parts[i])

            if error is not None:
                return

            cur_scope = value

            if cur_scope is None:
                return

        is_int = self.is_int(parts[-1])
        if is_int:
            idx = int(parts[-1])
            if isinstance(cur_scope, list):
                if idx > len(cur_scope):
                    error = parts[-1] + " index out of range"
                elif idx == len(cur_scope):
                    cur_scope.append(input)
                else:
                    cur_scope[idx] = input
            else:
                error = "set value for an index to a non-list object"

            if error is not None:
                return
        else:
            error = FunctionUtils.set_property(cur_scope, parts[-1], input).error
            if error is not None:
                return

        return

    def version(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        return json.dumps(self.memory)

    def is_int(self, int_str: str) -> bool:
        try:
            int(int_str)
            return True
        except ValueError:
            return False
