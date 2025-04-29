from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
# from herodetailmodel import HeroDetailModel, convert_row_to_heroesdetail
# from heromainmodel import HeroMainModel, convert_row_to_heroesmain
from heromainmodel import HeroMainModel
from typing import List
from herofullmodel import HeroFullModel, convert_row_to_heroes
from Itemsfullmodel import ItemFullModel, convert_row_to_item

import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()
tags_metadata = [
    {
        "name": "default",
        "description": "Endpoints กลุ่มทั่วไป (ยังไม่กำหนด tags)"
    },
    {
        "name": "heroes",
        "description": "จัดการข้อมูลฮีโร่"
    },
    {
        "name": "items",
        "description": "จัดการข้อมูลไอเท็ม"
    },
]

app = FastAPI(
    title="MobileLegend API",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url=None
)

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
@app.get(
    "/heroes/{hero_id}",
    response_model=HeroFullModel,
    tags=["heroes"],
    summary="ดึงฮีโร่ตามไอดี",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่ทั้งหมดแบบ nested structure"
)
def get_hero_by_id(hero_id: str):
    doc = heroes_collection.find_one({"Hero_ID": hero_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Hero not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_heroes(flat)
# ------------------- HEROES -----------------------------
@app.get(
    "/heroes",
    response_model=List[HeroFullModel],
    tags=["heroes"],
    summary="ดึงข้อมูลฮีโร่ทั้งหมด",
    description="คืนรายการฮีโร่ทุกตัวพร้อมรายละเอียดครบทุกฟิลด์"
)
def list_all_heroes():
    docs = list(heroes_collection.find())
    heroes = []
    for doc in docs:
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        heroes.append(convert_row_to_heroes(flat))
    return heroes
    
# -------------------- Heroesmain_id HEROESMain ROUTES --------------------
@app.get(
    "/heroesmain/{hero_id}",
    response_model=HeroFullModel,
    tags=["heroes"],
    summary="ดึงฮีโร่ตามไอดี",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่ทั้งหมดแบบ nested structure"
)
def get_hero_heroesmain(hero_id: str):
    doc = heroes_collection.find_one({"Hero_ID": hero_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Hero not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_heroes(flat) 
# ------------------------ HEROESMain ROUTES ----------------------------
@app.get(
    "/heroesmain",
    response_model=List[HeroMainModel],
    tags=["heroes"],
    summary="ดึงข้อมูลฮีโร่บางส่วน",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่ทั้งหมดแบบ nested structure"
)
def list_all_heroes():
    docs = list(heroes_collection.find())
    heroes = [
        HeroMainModel(
            hero_id=doc.get("Hero_ID", ""),
            hero_name=doc.get("HeroName", ""),
            role=doc.get("Role", ""),
            specialty=doc.get("Specialty", ""),
            lane_recc=doc.get("Lane_Recc", ""),
            icon=doc.get("Iconhero", ""),
            full=doc.get("Imagehero", "")
        )
        for doc in docs
    ]
    return heroes

# @app.get("/heroesmain", response_model=List[HeroMainModel])
# def list_all_heroes():
#         docs = list(heroes_collection.find())
#         heroes = []
#         for doc in docs:
#             flat = {k: str(v) for k, v in doc.items() if k != "_id"}
#             heroes.append(convert_row_to_heroesmain(flat))
#         return heroes
    
# # -------------------- HeroesDetail_id HEROESDetail ROUTES --------------------
# @app.get("/heroesdetail/{hero_id}", response_model=HeroFullModel) #ตัวดึง Hero_ID
# def get_hero_heroesdetail(hero_id: str):
#     doc = heroes_collection.find_one({"Hero_ID": hero_id})
#     if not doc:
#         raise HTTPException(status_code=404, detail="Hero not found")
#     flat = { k: str(v) for k, v in doc.items() if k != "_id" }
#     return convert_row_to_heroes(flat)

# # ------------------------ HEROESDetail ROUTES ----------------------------
# @app.get("/heroesdetail", response_model=List[HeroDetailModel])
# def list_all_heroes():
#     docs = list(heroes_collection.find())
#     heroes = []
#     for doc in docs:
#         flat = { k: str(v) for k, v in doc.items() if k != "_id" }
#         heroes.append(convert_row_to_heroesdetail(flat))
#     return heroes

# ----------------- Item_id ITEMS ROUTES ------------------
@app.get(
    "/items/{item_id}", 
    response_model=ItemFullModel,
    tags=["items"],
    summary="ดึงไอเทมตามไอดี",
    description="รับ Item_ID แล้วคืนข้อมูลไอเทมทั้งหมดแบบ nested structure"
)
def get_item_full(item_id: str):
    doc = items_collection.find_one({"Item_ID": item_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")
    flat = { k: str(v) for k, v in doc.items() if k != "_id" }
    return convert_row_to_item(flat)

# -------------------- ITEMS ROUTES --------------------
@app.get(
    "/items", 
    response_model=List[ItemFullModel],
    tags=["items"],
    summary="ดึงข้อมูลไอเทมทั้งหมด",
    description="คืนรายการไอเทมทุกอย่างพร้อมรายละเอียดครบทุกฟิลด์"
)
def list_all_items():
    docs = list(items_collection.find())
    items = []
    for doc in docs:
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        items.append(convert_row_to_item(flat))
    return items
