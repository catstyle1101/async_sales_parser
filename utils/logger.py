import logging
import sys


def create_logger() -> None:
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(filename='parser.log', encoding='utf-8', mode='a')
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    file_handler.setLevel(logging.WARNING)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
