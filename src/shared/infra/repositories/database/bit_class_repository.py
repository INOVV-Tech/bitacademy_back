from src.shared.infra.external.dynamo_datasource import DynamoDatasource

from src.shared.domain.repositories.bit_class_repository_interface import IBitClassRepository

from src.shared.domain.entities.bit_class import BitClass

class BitClassRepositoryDynamo(IBitClassRepository):
    dynamo: DynamoDatasource

    @staticmethod
    def bit_class_partition_key_format(bit_class: BitClass) -> str:
        return f'BIT_CLASS#{bit_class.title}'
    
    @staticmethod
    def bit_class_sort_key_format(bit_class: BitClass) -> str:
        return bit_class.created_at
    
    def __init__(self, dynamo: DynamoDatasource):
        self.dynamo = dynamo

    def create(self, bit_class: BitClass) -> BitClass:
        pass

    def get_all(self) -> list[BitClass]:
        pass
    
    def get_one(self, title: str) -> BitClass:
        pass

    def update(self, bit_class: BitClass) -> BitClass:
        pass

    def delete(self, bit_class: BitClass) -> BitClass:
        pass