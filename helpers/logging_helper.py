import logging
import os
import sys
import time

from configs import LOG_DIR


class LoggerHelper:
    def __init__(self):
        os.makedirs(LOG_DIR, exist_ok=True)
        self._setup_logger()

    def _setup_logger(self):
        runtime = time.strftime("%Y-%m-%d")
        logfile_debug = os.path.join(LOG_DIR, f"{runtime}.log")
        logfile_err = os.path.join(LOG_DIR, f"{runtime}_error.log")

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.handlers = []

        self._add_handler(logger, logfile_debug, logging.DEBUG)
        self._add_handler(logger, logfile_err, logging.ERROR, mode="a+")
        self._add_handler(logger, sys.stdout, logging.INFO, stream=True)

    def _add_handler(self, logger, path, level, mode="a+", stream=False):
        handler = (
            logging.StreamHandler(path) if stream else logging.FileHandler(path, mode)
        )
        handler.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s - %(levelname)s: %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)
