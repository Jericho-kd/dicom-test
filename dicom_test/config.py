import dotenv
from pathlib import Path


config_path = Path(__file__).resolve().parents[1]
config_env = dotenv.dotenv_values(config_path / '.env')

DICOM_PORT = int(config_env.get('DICOM_PORT'))
DICOM_TITLE = config_env.get('DICOM_TITLE')

OUTPUT_DIR = Path(config_env.get('OUTPUT_DIR'))

STORAGE_IP = config_env.get('STORAGE_IP')
STORAGE_TITLE = config_env.get('STORAGE_TITLE')