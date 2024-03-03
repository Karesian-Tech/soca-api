from src.common.base.repository import Repository


class Service:
    repository: Repository

    def __init__(self, repository: Repository):
        self.repository = repository
