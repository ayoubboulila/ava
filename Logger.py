import logging
from logging.handlers import RotatingFileHandler

logLevel = logging.DEBUG
#logLevel = logging.INFO



def RCLog(name):
    # create the logger object
    logger = logging.getLogger(name)
    # set debug level to print all logs
    logger.setLevel(logLevel)
    
    # create the formatter which will print time, loglevel and the message
    formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s: %(message)s')
    # create a handler to redirect the logs to a file in append mode with 1 backup and max size 1Mo
    
    file_handler = RotatingFileHandler('logs.log', 'a', 1000000, 1)

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    # create second handler which will redirect every log write to stdout

    steam_handler = logging.StreamHandler()
    steam_handler.setLevel(logging.DEBUG)
    steam_handler.setFormatter(formatter)
    logger.addHandler(steam_handler)
    return logger
    
    
    