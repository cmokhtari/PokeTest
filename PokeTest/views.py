import logging

from django.conf import settings

from logging.handlers import RotatingFileHandler


def setup_logger(
    logger_name,
    log_file,
    file_size,
    backup_nb,
    level=logging.INFO
):
    """To setup as many loggers as you want"""
    # backup_nb must be at least equal to 1 if you want to set a file max size
    # Because if backupCount is equal to 0 then the rotation is never triggered
    # and maxBytes is not used
    handler = RotatingFileHandler(
        f'{settings.BASE_DIR}/logs/{log_file}',
        maxBytes=file_size,
        backupCount=backup_nb
    )
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s : %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
