import os
import json

from dotenv import load_dotenv

from db_access.db_access import ProviderSQL

load_dotenv()

CWD = os.getcwd()
CONFIG_DIR = os.getenv('CONFIG_DIR')
DB_CONFIG = json.load(open(f'{CWD}/{CONFIG_DIR}/db_config.json', 'r'))
ACCESS_CONFIG = json.load(open(f'{CWD}/{CONFIG_DIR}/access.json', 'r'))
SQL_REQUESTS_DIR = os.getenv('SQL_REQUESTS_DIR')

sql_provider = ProviderSQL(f'{CWD}/{SQL_REQUESTS_DIR}')

ROOMS_AMOUNT = 2
MAX_PATIENTS_IN_ROOM = 2
