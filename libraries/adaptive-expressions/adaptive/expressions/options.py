class Options:
    null_substitution = None

    def __init__(self, opt=None):
        self.null_substitution = opt.null_substitution if opt is not None else None
