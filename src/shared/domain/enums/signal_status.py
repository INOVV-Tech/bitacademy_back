from enum import Enum

class SIGNAL_STATUS(Enum):
    ENTRY_WAIT = 'ENTRY_WAIT'
    RUNNING = 'RUNNING'
    DONE = 'DONE'

    @staticmethod
    def length() -> int:
        return len(SIGNAL_STATUS)