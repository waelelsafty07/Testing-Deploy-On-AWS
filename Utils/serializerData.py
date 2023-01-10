class serializerData():
    def __init__(self, model):
        self.model = model

    def Get(self):
        serializer = self.model
        return serializer

    def Post(self, raise_exception):
        serializer = self.model
        serializer.is_valid(raise_exception=raise_exception)
        return serializer
