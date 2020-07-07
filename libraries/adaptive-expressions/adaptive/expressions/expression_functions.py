class ExpressionFunctions:
    @staticmethod
    def access_index(instance: object, index: int):
        value: object = None
        error: str = None

        if instance is None:
            return value, error

        if isinstance(instance, list):
            if index >= 0 and index < len(instance):
                value = instance[index]
            else:
                error = str(index) + ' is out of range for ' + instance
        else:
            error = instance + ' is not a collection.'

        return value, error

    @staticmethod
    def access_property(instance: object, property: str):
        value: object = None
        error: str = None

        if instance is None:
            return value, error

        #TODO

        return value, error
