import logging
import os
from datetime import datetime

class ClassnameFormatter(logging.Formatter):
    def __init__(self, fmt, datefmt=None, style='%', classname=None):
        super().__init__(fmt, datefmt, style)
        self.classname = classname

    def format(self, record):
        if 'funcName' in record.__dict__:
            fn = record.__dict__['funcName']
            if self.classname is not None:
                fn = self.classname + "." + fn
            record.__dict__['funcName'] = fn
        return super().format(record)

def get_logger(name, class_name=None):
    # Create a logger
    logger = logging.getLogger(name)

    # Set the level of severity that will be logged
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    today = datetime.now()
    week_number = today.isocalendar()[1]
    year = today.year
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{week_number}_{year}.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.DEBUG)

    # Create a logging format
    formatter = ClassnameFormatter('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d - %(message)s',
                                   datefmt='%Y-%m-%d %H:%M:%S', classname=class_name)
    handler.setFormatter(formatter)

    # Check if the logger already has the handler to avoid duplicate logs
    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger