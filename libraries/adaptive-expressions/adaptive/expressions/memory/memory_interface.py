class MemoryInterface:
    def get_value(self, path: str) -> object:
        pass

    def set_value(self, path: str, input: object):
        pass

    def version(self) -> str:
        pass
