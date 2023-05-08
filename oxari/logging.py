

from datetime import datetime
import logging


class CustomUvicornFormatter(logging.Formatter):
    GREEN = "\033[32m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        microseconds = int(dt.microsecond / 1000)

        # Calculate timezone offset and format it
        offset = dt.utcoffset()
        if offset is not None:
            hours, remainder = divmod(offset.seconds, 3600)
            offset_str = f"{hours:+03d}:{remainder // 60:02d}"
        else:
            offset_str = "+00:00"

        formatted_time = dt.strftime(f"{self.GREEN}%Y-%m-%dT%H:%M:%S.{microseconds:03d}") + offset_str + self.RESET
        return formatted_time

    def format(self, record):
        record.levelname = f"{self.BOLD}{record.levelname}{self.RESET}"
        record.name = f"{self.BOLD}{record.name}{self.RESET}"
        return super().format(record)

def configure_logging():
    log_format = CustomUvicornFormatter(
        "%(asctime)s | %(levelname)-14s | %(name)s | %(message)s"
    )

    uvicorn_access_handler = logging.StreamHandler()
    uvicorn_access_handler.setFormatter(log_format)

    uvicorn_error_handler = logging.StreamHandler()
    uvicorn_error_handler.setFormatter(log_format)

    logging.getLogger("uvicorn.access").handlers = [uvicorn_access_handler]
    logging.getLogger("uvicorn.error").handlers = [uvicorn_error_handler]
