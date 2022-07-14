from rental_bike_share.constants import *
from datetime import datetime
import logging
import os

CURRENT_TIME_STAMP=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
LOG_DIR="logs"
LOG_FILE_NAME=f"log_{CURRENT_TIME_STAMP}.log"
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE_NAME)

os.makedirs(LOG_DIR,exist_ok=True)

logging.basicConfig(filename=LOG_FILE_PATH,filemode="w",level=logging.INFO,
                    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s")
