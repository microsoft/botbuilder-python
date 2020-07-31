from ..memory_interface import MemoryInterface


class StackedMemory(MemoryInterface, list):
    @staticmethod
    def wrap(memory: MemoryInterface):
        if isinstance(memory, StackedMemory):
            return memory

        stacked_memory = StackedMemory()
        stacked_memory.append(memory)

        return stacked_memory

    def get_value(self, path: str) -> object:
        if len(self) == 0:
            return None
        else:
            for memory in self[::-1]:
                if memory.get_value(path) is not None:
                    return memory.get_value(path)

            return None

    def set_value(self, path: str, input: object):
        raise Exception("Can't set value to " + path + ", stacked memory is read-only")

    def version(self) -> str:
        return "0"
