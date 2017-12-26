# coding=utf-8

import logging
from logging.handlers import RotatingFileHandler


# 日志打印
def init_logger(app):
    handler = RotatingFileHandler('logs/photohub.log', maxBytes=1024 * 1024 * 2, backupCount=2)
    logging_format = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
