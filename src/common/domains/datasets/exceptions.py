class DatasetItemsIsEmpty(Exception):
    "Raised when DatasetItems is empty"

    def __init__(self, message="DatasetItems is empty") -> None:
        self.message = message
        super().__init__(self.message)
