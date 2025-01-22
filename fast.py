from fastapi import *
from motor.motor_asyncio import AsyncIOMotorClient
from calculate import*
from key import*
import logging
from database import*
import schedule
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import asyncio


from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

class CustomBaseModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
        arbitrary_types_allowed=True  # Allow arbitrary types like ObjectId
    )

app = FastAPI()

# Example MongoDB client setup (replace with your MongoDB URI)
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["mydatabase"]

# Example model using CustomBaseModel
class ExampleModel(CustomBaseModel):
    id: ObjectId = Field(default_factory=ObjectId)  # Use ObjectId as a field

app = FastAPI()

# MongoDB connection

collection = db['Pricelist']

# Function to get item data from the database
async def get_item_from_db(sku):
    return await collection.find_one({"sku": sku},{'_id':0})

# Function to get all items from the database
async def get_all_items_from_db():
    

    return await collection.find({},{'_id':0}).to_list(length=None)  # Fetch all documents
    

# Dummy function for fetching price externally (you should replace with actual logic)
async def get_price(sku, external_sio=None):
    # Implement logic to fetch price externally
    

    sku_name = Sku.sku_to_name(sku)
    
    if sku=='5021;6':
        return await calculate_buy_sell_price(sku_name)  
    else:      

        return await calculate_sell_price(sku_name)

# Dummy functions to simulate attribute fetching (replace with actual logic)
'''def getAttributesBySKU(sku):
    return {"defindex": 1, "quality": "Unique"}'''  # Example attributes

def getNameBySKU(sku):
    return sku.sku_to_name(sku)  # Example name

@app.get("/items/{sku}", tags=['items'])
async def get_item_data(sku: str):
    # Try to fetch item from the database
    
    data = await get_item_from_db(sku)
    if data is None:
        # If not in database, fetch price externally
        data = await get_price(sku)

        await collection.insert_one(data)
        if data is None:
            raise HTTPException(status_code=404, detail="Not found")
    return data

@app.post("/items/{sku}", tags=['items'])
async def add_item(sku: str, background_tasks: BackgroundTasks):
    
        # Add background task to fetch the price
    background_tasks.add_task(get_price, sku)
    return {
        "success": True,
        "name": sku.sku_to_name(sku),
        "sku": sku
    }

@app.get("/items", tags=['items'])
async def get_price_list():

    items = await get_all_items_from_db()
    logging.info(items)
    return {
        'success': True,
        'currency': None,
        'items': items
    }






'''def update_all():
    update_database()
    pass

def startup_event():
    schedule.every(15).seconds.do(update_all)  # Run update_all every 30 minutes

def shutdown_event():
    schedule.cancel_job(update_all)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

import threading
thread = threading.Thread(target=run_schedule)
thread.daemon = True  # Set as daemon so it exits when main thread exits
thread.start()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)'''
async def update_all():
     update_database()  # Ensure update_database is an async function if it contains async calls

# Initialize APScheduler
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup_event():
    # Add the job to run every 15 seconds
    scheduler.add_job(update_all, trigger=IntervalTrigger(seconds=15))
    scheduler.start()  # Start the scheduler

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
sio=socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
async_handlers=True
)
pricer=socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app,
    socketio_path='/socket.io'
)
