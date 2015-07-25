from __future__ import absolute_import, unicode_literals

import logging
from logging import Logger, handlers

class YahooLogger(logging.Logger):
    """Yahoo Logger class
    """

    def __init__(self, name, level=logging.DEBUG,filename=None, log_file_size=5*1024*1024):
        """
        - name : logger name
        - filename : file containing logs
        """
        super(YahooLogger, self).__init__(name)
        self.name = name
        self.level = level

        self.setLevel(self.level)
        
        formatter = logging.Formatter("[%(asctime)s %(levelname)s] [%(name)s.%(module)s.%(funcName)s] %(message)s")
        if filename:
            file_handler = handlers.RotatingFileHandler(filename, 'w', log_file_size, 10)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.addHandler(stream_handler)

