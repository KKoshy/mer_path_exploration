"""
This file contains function essential for logger configuration
"""
import logging

from lib.common import LOG_FILE


def get_logger():
    """
    Configures log file and console logging
    :return: None
    """

    logging.basicConfig(
        filename=LOG_FILE,
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - " "%(levelname)s - %(message)s",
    )
    logger = logging.getLogger("mer_path_exploration.log")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log_format = "%(filename)s:%(lineno)s - %(funcName)5s() ]%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
