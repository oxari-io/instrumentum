from datetime import datetime
from datetime import timezone
import uvicorn
from fastapi import FastAPI
import logging

from oxari.fomatter import CustomFormatter

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


log_config = uvicorn.config.LOGGING_CONFIG
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
    log_config["loggers"][logger_name]["handlers"] = ["custom"]
    log_config["handlers"]["custom"] = {
        "class": "logging.StreamHandler",
        "formatter": "custom",
    }
    log_config["formatters"]["custom"] = {
        "()": CustomFormatter,
    }

# Disable propagation for "uvicorn.access" and "uvicorn.error" loggers
log_config["loggers"]["uvicorn.access"]["propagate"] = False
log_config["loggers"]["uvicorn.error"]["propagate"] = False

# Run the FastAPI app with Uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
