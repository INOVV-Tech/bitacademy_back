from src.shared.environments import Environments

def encode_idx_pk(pk: str) -> str:
    if not Environments.persist_local:
        return pk
    
    return '_'.join(pk.split('#'))