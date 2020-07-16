from .memory_interface import MemoryInterface


class Extensions:
    @staticmethod
    def is_memeory_interface(obj) -> bool:
        if obj is None:
            return False

        return isinstance(obj, MemoryInterface)
