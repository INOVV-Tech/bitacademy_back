from enum import Enum
import os
from dotenv import load_dotenv

class STAGE(Enum):
    TEST = "TEST"
    DEV = "DEV"
    QA = "QA"
    HOMOLOG = "HOMOLOG"
    PROD = "PROD"

class Environments:
    load_dotenv()
    stage: STAGE = STAGE(os.environ.get('STAGE', STAGE.TEST.value))
    db_url: str = os.environ.get("POSTGRES_URL", "postgresql://admin:admin@localhost:11000/geoinfra-test")