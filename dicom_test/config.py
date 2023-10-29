import dotenv
from pathlib import Path


config_path = Path(__file__).resolve().parents[1]
config_env = dotenv.dotenv_values(config_path / '.env')

OUTPUT_DIR = Path(config_env.get('OUTPUT_DIR'))
STORAGE_IP = config_env.get('STORAGE_IP')
STORAGE_NAME = config_env.get('STORAGE_NAME')