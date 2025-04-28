from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from herodetailmodel import HeroDetailModel, convert_row_to_heroesdetail
from heromainmodel import HeroMainModel, convert_row_to_heroesmain
from typing import List
from herofullmodel import HeroFullModel, convert_row_to_heroes
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
heroes_collection = db["heroesinfos"]
items_collection = db["itemsInfos"]


def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

# ------------------ Heroes_id HEROES --------------------
@app.get("/heroes/{hero_id}", response_model=HeroFullModel) #ตัวดึง Hero_ID
def get_hero_by_id(hero_id: str):
    doc = heroes_collection.find_one({"Hero_ID": hero_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Hero not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_heroes(flat)
# ------------------- HEROES -----------------------------
@app.get("/heroes", response_model=List[HeroFullModel])
def list_all_heroes():
    docs = list(heroes_collection.find())
    heroes = []
    for doc in docs:
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        heroes.append(convert_row_to_heroes(flat))
    return heroes
    
# -------------------- Heroesmain_id HEROESMain ROUTES --------------------
@app.get("/heroesmain/{hero_id}", response_model=HeroFullModel) #ตัวดึง Hero_ID
def get_hero_heroesmain(hero_id: str):
    doc = heroes_collection.find_one({"Hero_ID": hero_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Hero not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_heroes(flat) #แปลงเป็น HeroDetailModel
# ------------------------ HEROESMain ROUTES ----------------------------
@app.get("/heroesmain", response_model=List[HeroMainModel])
def list_all_heroes():
        docs = list(heroes_collection.find())
        heroes = []
        for doc in docs:
            flat = {k: str(v) for k, v in doc.items() if k != "_id"}
            heroes.append(convert_row_to_heroesmain(flat))
        return heroes
    
# -------------------- HeroesDetail_id HEROESDetail ROUTES --------------------
@app.get("/heroesdetail/{hero_id}", response_model=HeroFullModel) #ตัวดึง Hero_ID
def get_hero_heroesdetail(hero_id: str):
    doc = heroes_collection.find_one({"Hero_ID": hero_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Hero not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_heroes(flat)

# ------------------------ HEROESDetail ROUTES ----------------------------
@app.get("/heroesdetail", response_model=List[HeroDetailModel])
def list_all_heroes():
    docs = list(heroes_collection.find())
    heroes = []
    for doc in docs:
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        heroes.append(convert_row_to_heroesdetail(flat))
    return heroes

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
