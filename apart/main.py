from fastapi import FastAPI
from pymongo import MongoClient
from apart.routes.crud import router as crud_router
from apart.routes.func import router as func_router
import os
import logging


app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.environ['MONGO_URI'])
    app.database = app.mongodb_client[os.environ['DB_NAME']]
    logging.info("Connected to MongoDB database")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    logging.info("MongoDB connection closed")


app.include_router(crud_router, tags=["aparts"], prefix="/crud")
app.include_router(func_router, tags=["functionality"], prefix="/action")
