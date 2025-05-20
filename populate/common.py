import os
import base64
from pathlib import Path
from dotenv import load_dotenv

from src.shared.environments import Environments

def get_root_directory():
    return Path(__file__).parent.parent

def load_app_env(stage='DEV'):
    root_directory = get_root_directory()

    env_filepath = os.path.join(root_directory, 'iac', '.env')

    load_dotenv(env_filepath)
    
    os.environ['STAGE'] = stage

    Environments.reload()

def load_resource(filename, encode_base64=True, base64_prefix=''):
    root_directory = get_root_directory()

    filepath = os.path.join(root_directory, 'populate', '.resources', filename)

    data = open(filepath, 'rb').read()

    if encode_base64:
        data = base64.b64encode(data)
        data = data.decode('utf8')
        data = base64_prefix + ',' + data if len(base64_prefix) > 0 else data

    return data