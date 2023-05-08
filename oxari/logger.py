from datetime import datetime, timezone
import logging
import uvicorn

class OxariFormatter(logging.Formatter):
    COLOR_CODES = {
        'INFO': '\033[32m',  # Green
        'DEBUG': '\033[36m',  # Cyan
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[41m',  # Red background
    }
    RESET_CODE = '\033[0m'

    def format(self, record):
        dt = datetime.fromtimestamp(record.created).astimezone()
        utc_dt = dt.astimezone(timezone.utc)
        microseconds = int(utc_dt.microsecond / 1000)
        offset_str = utc_dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{microseconds:03d}" + dt.strftime("%z")

        level_name = record.levelname
        message = record.getMessage()
        name = record.name

        colored_level_name = self.colorize_level_name(level_name)

        return f"{offset_str} | {colored_level_name:<5} | {name} | {message}"

    def colorize_level_name(self, level_name):
        color_code = self.COLOR_CODES.get(level_name, '')
        return f"{color_code}{level_name}{self.RESET_CODE}"


def generate_log_config():
    log_config = uvicorn.config.LOGGING_CONFIG
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