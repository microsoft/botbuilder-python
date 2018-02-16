class EmulatorValidation:
    def __init__(self):
        self.foo = None

    @staticmethod
    def is_from_emulator(header):
        return True

    @staticmethod
    def authenticate_token(header, credentials):
        pass