from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from herodetailmodel import HeroDetailModel
from heromainmodel import HeroMainModel
from typing import List
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
@app.get("/heroes/{hero_id}")
def get_hero_by_id(hero_id: str):
    try:
        hero = heroes_collection.find_one({"Hero_ID": hero_id}) # เป็นการดึงข้อมูลจาก heroes แทน heroesdetail
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return fix_id(hero)
    except Exception as e:
        print(f"[ERROR /heroesdetail]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

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

# -------------------- Heroesmain_id HEROESMain ROUTES --------------------
@app.get("/heroesmain/{hero_id}", response_model=HeroDetailModel)
def get_hero_heroesmain(hero_id: str):
    try:
        hero = heroes_collection.find_one({"Hero_ID": hero_id})  # เปลี่ยนเป็น heroes_collection
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return HeroDetailModel(**fix_id(hero))  # ใช้ HeroDetailModel
    except Exception as e:
        print(f"[ERROR /heroesmain]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# ------------------------ HEROESMain ROUTES ----------------------------
@app.get("/heroesmain", response_model=List[HeroMainModel])
def get_all_heroes_main():
    try:
        heroesmain = list(heroes_collection.find())
        return [HeroMainModel(**fix_id(heromain)) for heromain in heroesmain]  # ใช้ HeroMainModel
    except Exception as e:
        print(f"[ERROR /heroesmain]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/heroesmain/name/{name}", response_model=HeroMainModel)
def get_hero_by_name_main(name: str):
    try:
        heromain = heroes_collection.find_one({"HeroName": name})
        if not heromain:
            raise HTTPException(status_code=404, detail="Hero not found")
        return HeroMainModel(**fix_id(heromain))  # ใช้ HeroMainModel
    except Exception as e:
        print(f"[ERROR /heroesmain/name]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/heroesmain/type/{type_name}", response_model=List[HeroMainModel])
def get_heroes_by_type_main(type_name: str):
    try:
        heroesmain = list(heroes_collection.find({"Type": type_name}))
        if not heroesmain:
            raise HTTPException(status_code=404, detail=f"No heroes found in type: {type_name}")
        return [HeroMainModel(**fix_id(heromain)) for heromain in heroesmain]  # ใช้ HeroMainModel
    except Exception as e:
        print(f"[ERROR /heroesmain/type]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
        

# -------------------- HeroesDetail_id HEROESDetail ROUTES --------------------
@app.get("/heroesdetail/{hero_id}")
def get_hero_detail(hero_id: str):
    try:
        hero = heroes_collection.find_one({"Hero_ID": hero_id}) # เป็นการดึงข้อมูลจาก heroes แทน heroesdetail
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        return fix_id(hero)
    except Exception as e:
        print(f"[ERROR /heroesdetail]: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# ------------------------ HEROESDetail ROUTES ----------------------------
@app.get("/heroesdetail", response_model=List[HeroDetailModel])
def get_all_heroes_detail():
    heroesdetail = list(heroes_collection.find())  # เปลี่ยนเป็น heroes_collection
    return [HeroDetailModel(**fix_id(herodetail)) for herodetail in heroesdetail]

@app.get("/heroesdetail/name/{name}", response_model=HeroDetailModel)
def get_hero_by_name_detail(name: str):
    herodetail = heroes_collection.find_one({"HeroName": name})  # เปลี่ยนเป็น heroes_collection
    if not herodetail:
        raise HTTPException(status_code=404, detail="Hero not found")
    return HeroDetailModel(**fix_id(herodetail))

@app.get("/heroesdetail/type/{type_name}", response_model=List[HeroDetailModel])
def get_heroes_by_type_detail(type_name: str):
    heroesdetail = list(heroes_collection.find({"Type": type_name}))  # เปลี่ยนเป็น heroes_collection
    if not heroesdetail:
        raise HTTPException(status_code=404, detail=f"No heroes found in type: {type_name}")
    return [HeroDetailModel(**fix_id(herodetail)) for herodetail in heroesdetail]

