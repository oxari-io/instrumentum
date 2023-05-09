from datetime import datetime
from datetime import timezone
import uvicorn
from fastapi import FastAPI
import logging

from oxari.logger import generate_log_config, get_logger

app = FastAPI()

@app.get("/")
async def root():
    logger = get_logger()
    logger.setLevel('DEBUG')
    logger.info('I-Hello World')
    logger.warning('W-Hello World')
    logger.debug('D-Hello World')
    logger.error('E-Hello World')
    return {"message": "Hello World"}




log_config = generate_log_config()

# Run the FastAPI app with Uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
