from src.environments import STAGE, Environments

class Repository:
    def __init__(self):
        self.session = None

        if Environments.stage == STAGE.TEST:
            self._initialize_mock_repositories()
        else:
            self._initialize_database_repositories()

    def _initialize_mock_repositories(self):
        pass
        
    def _initialize_database_repositories(self):
        pass