class InvalidArgumentException(Exception):

    def __init__(self, message="Invalid argument"):
        self.message = message
        super().__init__(self.message)