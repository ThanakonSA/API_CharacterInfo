from fastapi import FastAPI, HTTPException, Body, Request, Form
from pymongo import MongoClient, DESCENDING, ReturnDocument
from fastapi.middleware.cors import CORSMiddleware
from models.setmodel import CreateItemBuild, PatchItemBuild, ItemBuild
from models.heromainmodel import HeroMainModel
from models.herofullmodel import HeroFullModel, convert_row_to_heroes
from models.Itemsfullmodel import ItemFullModel, ItemInfo, ItemMainModel, convert_row_to_item
from typing import List, Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient

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
    title="MLBB API",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url=None
)
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient("mongodb+srv://thanakon3:Teera0Chineseboi@cluster0.mft4otf.mongodb.net/")
db = client["MobileLegend_wiki_backend"]
heroes_collection = db["heroesinfos"]
items_collection = db["itemsInfos"]
setitems_collection = db["setitems"]


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")



def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc


items: List[ItemMainModel] = [
    ItemMainModel(iteminfo=itm) for itm in [
        # สร้าง ItemInfo ด้วยข้อมูลจริง
        # ตัวอย่าง:
        # ItemInfo(item_id="item1", item_name="Sword", type_item="Attack", price="1000", icon="/static/icons/item1.png")
    ]
]

# -------------------- Heroes_id HEROES ROUTES --------------------
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

# ------------------------ HEROES ROUTES ----------------------------
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

# -------------------- Heroesmian_id HEROESMain ROUTES --------------------
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



# -------------------- Item_id ITEMS ROUTES --------------------
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

# ------------------------- ITEMS ROUTES ----------------------------------
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

#----------------------------------------------------------------------
@app.get("/newsetitems", response_class=HTMLResponse)
async def new_set_items(request: Request):
    # ── ดึงฮีโร่จาก collection จริง ────────────────────────────────
    hero_docs = list(heroes_collection.find({}))
    heroes = [
        HeroMainModel(
            hero_id   = doc.get("Hero_ID", ""),
            hero_name = doc.get("HeroName", ""),
            role      = doc.get("Role", ""),
            specialty = doc.get("Specialty", ""),
            lane_recc = doc.get("Lane_Recc", ""),
            icon      = doc.get("Iconhero", ""),
            full      = doc.get("Imagehero", "")
        )
        for doc in hero_docs
    ]

    # ── ดึงไอเท็มจาก collection จริง ───────────────────────────────
    item_docs = list(items_collection.find({}))
    items = [
        ItemMainModel(
            iteminfo=ItemInfo(
                item_id   = doc.get("Item_ID", ""),
                item_name = doc.get("ItemName", ""),
                type_item = doc.get("Type_Item", ""),
                price     = str(doc.get("Price", "")),
                icon      = doc.get("Icon_Item", "")
            )
        )
        for doc in item_docs
    ]
    existing = setitems_collection.find_one(
       sort=[("setitems_id", DESCENDING)]
    )

    return templates.TemplateResponse("newsetitems.html", {
        "request": request,
        "heroes": heroes,
        "items": items,
        "existing": existing
    })

# รับข้อมูลฟอร์มเมื่อกด Submit
@app.post("/newsetitems")
def create_set_items(
    hero_id: str = Form(...),
    hero_name: str = Form(...),
    item1:   str = Form(None),
    item2:   str = Form(None),
    item3:   str = Form(None),
    item4:   str = Form(None),
    item5:   str = Form(None),
    item6:   str = Form(None),
):
    # 1) เก็บเฉพาะไอดีที่เลือกมา
    raw_ids = [item1, item2, item3, item4, item5, item6]
    ids     = [i for i in raw_ids if i]

    # 2) ดึงข้อมูลเต็มจาก collection itemsInfos แล้วสร้าง ItemMainModel
    items_models = []
    for iid in ids:
        doc = items_collection.find_one({"Item_ID": iid})
        if not doc:
            continue
        info = ItemInfo(
            item_id   = doc.get("Item_ID", ""),
            item_name = doc.get("ItemName", ""),
            type_item = doc.get("Type_Item", ""),
            price     = str(doc.get("Price", "")),
            icon      = doc.get("Icon_Item", "")
        )
        items_models.append(ItemMainModel(iteminfo=info).dict())

    record = {
        "hero_id":     hero_id,
        "hero_name":   hero_name,
        "items":       items_models
    }

    # 5) บันทึกลง MongoDB (sync PyMongo)
    setitems_collection.insert_one(record)

    # 6) ส่งกลับหรือ redirect ตามต้องการ
    return RedirectResponse("/newsetitems?success=1", status_code=303)

#--------------------- Setitems SETITEMS ROUTES --------------------
# ——— ดึงชุดไอเทมตาม id ———
@app.get(
    "/setitems",
    response_model=List[ItemBuild],
    summary="ดึงข้อมูลชุดไอเทมทั้งหมด",
    description="คืนค่าเป็นลิสต์ของทุกเซตไอเทมในฐานข้อมูล"
)
def list_item_builds():
    # ไม่กรองด้วย setitems_id, และตัด _id ออก
    docs = list(setitems_collection.find({}, {"_id": 0}))
    return docs
    
#--------------------- Setitems_id SETITEMS ROUTES --------------------
@app.get(
    "/setitems/{hero_id}",
    response_model=List[ItemBuild],
    summary="ดึงชุดไอเท็มของฮีโร่โดย hero_id",
    description="รับ hero_id ใน path → คืนชุดไอเท็มทั้งหมดที่เก็บไว้สำหรับฮีโร่คนนั้น"
)
def get_setitems_by_hero(hero_id: str):
    """
    1. @app.get("/setitems/{hero_id}")  
       - กำหนดว่า endpoint นี้รับ HTTP GET บน URL /setitems/<hero_id>  
       - ค่าใน {} จะถูกแมปเป็นตัวแปร hero_id ของฟังก์ชัน  

    2. response_model=List[ItemBuild]  
       - บอก FastAPI ให้ใช้ Pydantic Model `ItemBuild` ในการตรวจสอบ (validation)  
       - List[...] แปลว่าคืนเป็นลิสต์ของ ItemBuild  

    3. def get_setitems_by_hero(hero_id: str):  
       - ฟังก์ชันนี้รับพารามิเตอร์ hero_id (string)  

    4. docs = list(setitems_collection.find(
           {"hero_id": hero_id},     # เงื่อนไขค้นว่าฟิลด์ hero_id ในเอกสารต้องเท่ากับค่าที่ path ส่งมา
           {"_id": 0}                # projection: ตัด _id ของ MongoDB ออก ไม่ส่งกลับให้ client
       ))
       - `find()` จะคืน cursor ของหลายเอกสาร
       - เราแปลงเป็น Python list เพื่อเตรียม return  

    5. if not docs:
         raise HTTPException(
             status_code=404,
             detail=f"No setitems found for hero_id={hero_id}"
         )
       - ถ้าไม่มีเอกสารชุดไหนเลย ให้ตอบ 404 Not Found พร้อมข้อความ  

    6. return docs
       - คืนลิสต์ของ dict ที่ตรงกับโครงสร้าง ItemBuild
    """
    docs = list(setitems_collection.find(
        {"hero_id": hero_id},
        {"_id": 0}
    ))

    if not docs:
        # ถ้าไม่เจอชุดไอเท็มของ hero_id นี้เลย
        raise HTTPException(
            status_code=404,
            detail=f"No setitems found for hero_id={hero_id}"
        )

    return docs


#-------------------- edit setitems_id SETITEMS ROUTES --------------------
@app.put(
    "/sets/{set_id}",
    response_model=CreateItemBuild,
    summary="อัปเดตเซตไอเทม",
)
def update_item_build(set_id: int, payload: CreateItemBuild):
    # ยืนยันว่ามีชุดนี้อยู่
    existing = setitems_collection.find_one({"setitems_id": set_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Set not found")

    # ดึงข้อมูลไอเทมใหม่
    items = []
    for iid in payload.item_ids:
        doc = items_collection.find_one({"Item_ID": iid})
        if not doc:
            raise HTTPException(status_code=404, detail=f"Item {iid} not found")
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        items.append(convert_row_to_item(flat))

# อัปเดตใน Mongo
    updated = {
        "hero_id": payload.hero_id,
        "items":   [item.dict() for item in items]
    }
    setitems_collection.update_one(
        {"setitems_id": set_id},
        {"$set": updated}
    )
    # ส่งกลับข้อมูลใหม่
    return {**{"setitems_id": set_id}, **updated}
#-----------------------------------------------------------------------
@app.patch(
    "/sets/{set_id}",
    response_model=CreateItemBuild,
    summary="อัปเดตเฉพาะบางฟิลด์ของชุดไอเทม",
)
def patch_item_build(set_id: int, payload: PatchItemBuild):
    # 1) ดึงของเดิมมาจาก DB
    doc = setitems_collection.find_one({"setitems_id": set_id}, {"_id": 0})
    if not doc:
        raise HTTPException(404, "Set not found")

    update_data = {}
    # 2) ถ้ามี hero_id ใหม่ ให้อัปเดต
    if payload.hero_id is not None:
        update_data["hero_id"] = payload.hero_id

    # 3) ถ้ามี item_ids ใหม่ ให้เช็กความยาวและอัปเดต
    if payload.item_ids is not None:
        if len(payload.item_ids) != 6:
            raise HTTPException(422, "item_ids ต้องมี 6 ช่อง")
        # (คุณอาจจะต้องดึงรายละเอียดจาก itemsInfos เหมือน POST/PUT)
        update_data["items"] = payload.item_ids  # หรือแปลงเป็น full model เหมือนเดิม

    # 4) ถ้าไม่มีอะไรให้แก้เลย
    if not update_data:
        raise HTTPException(400, "ไม่มีข้อมูลอะไรให้อัปเดต")

    # 5) บันทึกลง DB
    setitems_collection.update_one(
        {"setitems_id": set_id},
        {"$set": update_data}
    )

    # 6) ดึงของใหม่ส่งกลับ
    return setitems_collection.find_one({"setitems_id": set_id}, {"_id": 0})
