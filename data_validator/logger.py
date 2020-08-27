import logging
import os

def config_logger(path):
    log_name = 'validator_log.txt'
    log_filename = os.path.join(path, log_name)
    LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
    logging.basicConfig(filename = log_filename, level=logging.DEBUG, format=LOG_FORMAT)
    logger = logging.getLogger()
    return logger