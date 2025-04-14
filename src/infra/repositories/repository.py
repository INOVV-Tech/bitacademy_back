from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from domain.repositories.address_repository_interface import IAddressRepository
from domain.repositories.user_repository_interface import IUserRepository
from infra.repositories.database.address_repository_db import AddressRepositoryDb
from infra.repositories.database.user_repository_db import UserRepositoryDb
from infra.repositories.mocks.adress_repository_mock import AddressRepositoryMock
from infra.repositories.mocks.user_repository_mock import UserRepositoryMock
from src.environments import STAGE, Environments
from src.infra.external.postgre_datasource import PostgreDatasource
from src.helpers.errors.errors import DatabaseException


class Repository:
    user_repo: IUserRepository
    address_repo: IAddressRepository

    def __init__(
            self,
            user_repo: bool = False,
            address_repo: bool = False,
    ):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories(
                user_repo, address_repo
            )
        else:
            self._initialize_database_repositories(
                user_repo, address_repo
            )

    def _initialize_mock_repositories(self, user_repo, address_repo):
        if user_repo:
            self.user_repo = UserRepositoryMock()
        if address_repo:
            self.address_repo = AddressRepositoryMock()
        
    def _initialize_database_repositories(self, user_repo, address_repo):
        session = self.__connect_db()
        datasource = PostgreDatasource(session)
        if user_repo:
            self.user_repo = UserRepositoryDb(datasource)
        if address_repo:
            self.address_repo = AddressRepositoryDb(datasource)

    @staticmethod
    def __connect_db() -> Session:
        try:
            engine = create_engine(Environments.db_url, poolclass=NullPool)
            return Session(engine)
        except (SQLAlchemyError, Exception) as error:
            raise DatabaseException(f"{error}")

    def close_session(self):
        if self.session:
            self.session.close()
            self.session = None
    
    def __del__(self):
        self.close_session()