class Errors:
    _instance = None
    listErrors = []

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def addError(self, err):
        self.listErrors.append(err)

    def hasError(self) -> bool:
        return not (self.listErrors == [])
