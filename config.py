import os

from dotenv import load_dotenv


load_dotenv()
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
MAN_ID = os.getenv('MAN_ID')
BASE_URL = os.getenv('BASE_URL')
BASE_DOMAIN = os.getenv('BASE_DOMAIN')
DATE_INCREMENT = 3
DB_ADDRESS = os.getenv('DB_ADDRESS')
SEMAPHORE_VALUE = 20
