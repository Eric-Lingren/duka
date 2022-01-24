import logging


def create_debug_log(file, message):
    logging.basicConfig(
        filename = file, 
        encoding='utf-8', 
        level=logging.DEBUG
    )
    logging.debug(message)


def create_info_log(file, message):
    logging.basicConfig(
        filename = file, 
        encoding='utf-8', 
        level=logging.INFO
    )
    logging.info(message)


def create_warning_log(file, message):
    logging.basicConfig(
        filename = file, 
        encoding='utf-8', 
        level=logging.WARNING
    )
    logging.warning(message)


def create_error_log(file, message):
    logging.basicConfig(
        filename = file, 
        encoding='utf-8', 
        level=logging.ERROR
    )
    logging.error(message)

