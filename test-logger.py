from datetime import datetime
from datetime import timezone
import uvicorn
from fastapi import FastAPI
import logging

from oxari.logger import generate_log_config

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}




log_config = generate_log_config()

# Run the FastAPI app with Uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
