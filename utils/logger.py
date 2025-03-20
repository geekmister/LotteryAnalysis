import logging
import os

import utils.filemanager as filemanager

LOG_FILE_PATH = os.path.join(filemanager.get_project_root(), "log.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)