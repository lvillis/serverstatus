__all__ = ['logger']

import logging


class Log(object):
    def __init__(self, _logger=None):
        self._logger = logging.getLogger(_logger)
        self._logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d   [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
        ch.close()

    def get_logger(self):
        return self._logger


logger = Log().get_logger()
