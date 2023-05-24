from datetime import datetime, timezone
import logging


class OxariFormatter(logging.Formatter):
    COLOR_CODES = {
        'INFO': '\033[32m',  # Green
        'DEBUG': '\033[36m',  # Cyan
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[41m',  # Red background
    }
    RESET_CODE = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        dt = datetime.fromtimestamp(record.created).astimezone()
        utc_dt = dt.astimezone(timezone.utc)
        microseconds = int(utc_dt.microsecond / 1000)
        time_with_offset = utc_dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{microseconds:03d}" + dt.strftime("%z")

        level_name = record.levelname
        message = record.getMessage()
        name = f"{record.module}:{record.funcName}:{record.lineno}"

        color_code = self.COLOR_CODES.get(level_name, '')

        return f"{color_code}{level_name:.1}{self.RESET_CODE}: {time_with_offset} | {name} | {message}"


def generate_log_config() -> dict:
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO"
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False
            },
        },
    }
    handler = logging.StreamHandler()
    handler.setFormatter(OxariFormatter())

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        log_config["loggers"][logger_name]["handlers"] = ["custom"]
        log_config["handlers"]["custom"] = {
            "class": "logging.StreamHandler",
            "formatter": "custom",
        }
        log_config["formatters"]["custom"] = {
            "()": OxariFormatter,
        }

    # Disable propagation for "uvicorn.access" and "uvicorn.error" loggers
    log_config["loggers"]["uvicorn.access"]["propagate"] = False
    log_config["loggers"]["uvicorn.error"]["propagate"] = False
    return log_config


logger = logging.getLogger("oxari")
fh = logging.StreamHandler()
fh.setFormatter(OxariFormatter())
logger.addHandler(fh)


def get_logger() -> logging.Logger:
    return logger