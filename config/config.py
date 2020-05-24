import yaml
import os
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler

ENV = os.environ.get('FLASK_ENV')

with open('config/{}.yaml'.format(ENV)) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

DB_URI = "mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8".format(
    config['db']['user'],
    config['db']['password'],
    config['db']['host'],
    config['db']['port'],
    config['db']['database']
)


class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename):
        RotatingFileHandler.__init__(self, filename, maxBytes=1024 * 1024 * 200, backupCount=20, encoding='utf-8')


def init_logging_config():
    logging.handlers.DateFormatRotatingFileHandler = CustomRotatingFileHandler

    if ENV == 'local':
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(levelname)s %(process)d %(thread)d %(module)s:%(funcName)s:%(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.DateFormatRotatingFileHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "filename": "./log/company_info.log"
                }
            },
            "loggers": {
                "app": {
                    "level": "INFO",
                    "handlers": ["console", ],
                    "propagate": False
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", ]
            }
        }
        logging.config.dictConfig(logging_config)
    else:
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s %(levelname)s %(process)d %(thread)d %(module)s:%(funcName)s:%(lineno)d - %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.DateFormatRotatingFileHandler",
                    "level": "INFO",
                    "formatter": "simple",
                    "filename": "/opt/python/log/company_info.log"
                }
            },
            "loggers": {
                "app": {
                    "level": "INFO",
                    "handlers": ["console", ],
                    "propagate": False
                },
            },
            "root": {
                "level": "INFO",
                "handlers": ["console", ]
            }
        }

    logging.config.dictConfig(logging_config)
