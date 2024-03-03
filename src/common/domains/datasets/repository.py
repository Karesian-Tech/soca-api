from src.common.base.repository import Repository
from src.common.models.dataset import Dataset
from src.common.domains.datasets.entity import Dataset as DatasetDomain


class DatasetRepository(Repository):
    def __init__(self, model: Dataset, domain: DatasetDomain):
        super().__init__(model, domain)
