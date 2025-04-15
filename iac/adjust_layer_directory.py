import os
import shutil
import subprocess
from pathlib import Path

IAC_DIRECTORY_NAME = 'iac'
SOURCE_DIRECTORY_NAME = 'src'
LAMBDA_LAYER_PREFIX = os.path.join('python', 'src')
REQUIREMENTS_FILE = 'requirements.txt'

def adjust_layer_directory(shared_dir_name: str, destination: str):
    # Diretórios principais
    root_directory = Path(__file__).parent.parent
    iac_directory = os.path.join(root_directory, IAC_DIRECTORY_NAME)
    destination_directory = os.path.join(iac_directory, destination)

    # Criar as pastas necessárias para a Layer
    layer_python_directory = os.path.join(destination_directory, 'python')
    layer_src_directory = os.path.join(layer_python_directory, 'src')  # "src" dentro de "python"

    os.makedirs(layer_python_directory, exist_ok=True)
    os.makedirs(layer_src_directory, exist_ok=True)

    print(f'Root directory: {root_directory}')
    print(f'Creating layer directory: {layer_python_directory}')
    print(f'Creating src directory inside layer: {layer_src_directory}')
    
    # Instalar dependências na pasta "python/"
    requirements_path = os.path.join(root_directory, REQUIREMENTS_FILE)

    if os.path.exists(requirements_path):
        print(f'Installing dependencies from {requirements_path} into {layer_python_directory}...')

        subprocess.run(
            [ 'pip', 'install', '-r', requirements_path, '-t', layer_python_directory, '--platform', 'manylinux2014_x86_64', '--only-binary=:all:' ],
            check=True
        )
    else:
        print(f'❌ ERROR: Requirements file \'{REQUIREMENTS_FILE}\' not found!')

    # Copiar arquivos compartilhados para "python/src/"
    source_directory = os.path.join(root_directory, SOURCE_DIRECTORY_NAME, shared_dir_name)

    if os.path.exists(source_directory):
        shutil.copytree(source_directory, os.path.join(layer_src_directory, shared_dir_name), dirs_exist_ok=True)

        print(f'Copied shared directory: {source_directory} to {os.path.join(layer_src_directory, shared_dir_name)}')
    else:
        print(f'❌ ERROR: Shared directory \'{source_directory}\' not found!')

    print(f'✅ Layer directory prepared at: {layer_python_directory}')

if __name__ == '__main__':
    adjust_layer_directory(shared_dir_name='shared', destination='lambda_layer_out_temp')