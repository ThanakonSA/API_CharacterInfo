from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["MobileLegend_wiki_backend"]
heroes_collection = db["characterinfos"]
items_collection = db["itemInfo"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ------------------ _id HEROES --------------------
@app.get("/heroes/{hero_id}")
def get_hero_by_id(hero_id: str):
    from bson import ObjectId  # ยังคงต้องใช้สำหรับการค้นหา
    try:
        hero = heroes_collection.find_one({"_id": ObjectId(hero_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return fix_id(hero)  # แปลง _id เป็นสตริงก่อนส่งออก
# ------------------- HEROES -----------------------------
@app.get("/heroes")
def get_all_heroes():
    heroes = list(heroes_collection.find())
    return [fix_id(hero) for hero in heroes]

@app.get("/heroes/name/{name}")
def get_hero_by_name(name: str):
    hero = heroes_collection.find_one({"HeroName": name})
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return fix_id(hero)

@app.get("/heroes/type/{type_name}")
def get_heroes_by_type(type_name: str):
    heroes = list(heroes_collection.find({"Type": type_name}))
    if not heroes:
        raise HTTPException(status_code=404, detail=f"No heroes found in type: {type_name}")
    return [fix_id(hero) for hero in heroes]


# ----------------- _id ITEMS ROUTES ------------------
@app.get("/items/{item_id}")
def get_item_by_id(item_id: str):
    from bson import ObjectId  # ใช้สำหรับการค้นหา _id
    try:
        item = items_collection.find_one({"_id": ObjectId(item_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return fix_id(item)  # แปลง _id เป็นสตริงก่อนส่งออก

# -------------------- ITEMS --------------------
@app.get("/items")
def get_all_items():
    items = list(items_collection.find())
    return [fix_id(item) for item in items]

@app.get("/items/name/{name}")
def get_item_by_name(name: str):
    item = items_collection.find_one({"ItemName": name})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return fix_id(item)

@app.get("/items/type/{type_name}")
def get_items_by_type(type_name: str):
    items = list(items_collection.find({"Type": type_name}))
    if not items:
        raise HTTPException(status_code=404, detail=f"No items found in type: {type_name}")
    return [fix_id(item) for item in items]

