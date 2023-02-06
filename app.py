from fastapi import FastAPI
from routes.config import router as config_router

app = FastAPI()
app.include_router(config_router)
