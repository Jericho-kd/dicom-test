import dotenv
from pathlib import Path


config_path = Path(__file__).resolve().parents[1]
config_env = dotenv.dotenv_values(config_path / '.env')

OUTPUT_FOLDER = config_env.get('OUTPUT_FOLDER')
STORAGE_IP = config_env.get('STORAGE_IP')
STORAGE_NAME = config_env.get('STORAGE_NAME')