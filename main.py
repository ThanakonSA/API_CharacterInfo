from fastapi import FastAPI, HTTPException, Body, Request, Form, Depends, File, UploadFile
from pymongo import MongoClient, DESCENDING, ReturnDocument
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from models.setmodel import CreateItemBuild, PatchItemBuild, ItemBuild, NewSetItems
from models.heromainmodel import HeroMainModel
from models.herofullmodel import HeroFullModel, convert_row_to_heroes
from models.Itemsfullmodel import ItemFullModel, ItemInfo, ItemMainModel, convert_row_to_item
from models.add_hero_model import HeroForm, get_hero_form
from typing import List, Optional
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

tags_metadata = [
    {
        "name": "heroes",
        "description": "จัดการข้อมูลฮีโร่"
    },
    {
        "name": "items",
        "description": "จัดการข้อมูลไอเทม"
    },
    {
        "name": "setitems",
        "description": "ข้อมูลของเซตไอเทม"
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
setitems_collection  = db["setitems"]
counters_collection  = db["counters"]


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
    ]
]

# -------------------- Heroes_id HEROES ROUTES --------------------
@app.get(
    "/heroes/{hero_id}",
    response_model=HeroFullModel,
    tags=["heroes"],
    summary="ดึงฮีโร่ตามไอดี (full)",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่แบบเต็ม"
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
    summary="ดึงฮีโร่ตามไอดี (full)",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่แบบเต็ม"
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
    summary="ดึงฮีโร่ตามไอดี (main)",
    description="รับ Hero_ID แล้วคืนข้อมูลฮีโร่แบบย่อ"
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
    summary="ดึงฮีโร่ทั้งหมด (main)",
    description="คืนรายการฮีโร่ทุกตัวแบบย่อ (HeroMainModel)"
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
    description="รับ Item_ID แล้วคืนข้อมูลไอเทมทั้งหมด"
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
    summary="ดึงไอเทมทั้งหมด",
    description="คืนรายการไอเทมทุกชิ้นพร้อมรายละเอียด"
)
def list_all_items():
    docs = list(items_collection.find())
    items = []
    for doc in docs:
        flat = { k: str(v) for k, v in doc.items() if k != "_id" }
        items.append(convert_row_to_item(flat))
    return items

#-------------------- Build_Set_Items -----------------------------------
@app.get("/build_set_items", response_class=HTMLResponse,
        tags=["setitems"],
        summary="หน้า สร้างชุดไอเทม",
        description="แสดงฟอร์มเลือกฮีโร่+ไอเทม เพื่อสร้างชุดใหม่"
        )
async def build_set_items_page(request: Request):
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

    # ── ดึงไอเทมจาก collection จริง ───────────────────────────────
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
    sort=[("set", DESCENDING)]
    )

    return templates.TemplateResponse("build_set_items.html", {
        "request": request,
        "heroes": heroes,
        "items": items,
        "existing": existing
    })

# รับข้อมูลฟอร์มเมื่อกด Submit
@app.post(
    "/build_set_items",
    tags=["setitems"],
    summary="บันทึกชุดไอเทมใหม่",
    description="รับข้อมูลจากฟอร์มแล้ว insert ลง MongoDB"
)
async def build_set_items(request: Request):
    payload   = await request.json()
    hero_id   = payload["hero_id"]
    hero_name = payload["hero_name"]
    hero_icon = payload["hero_icon"]
    raw_items = payload.get("items", [])

    # ── Enrich ให้ข้อมูลเต็ม ────────────────────────────────
    enriched = []
    for it in raw_items:
        info    = it.get("iteminfo", it)      # รองรับทั้ง {iteminfo:{…}} หรือ {item_id:…}
        item_id = info.get("item_id")
        if not item_id:
            continue
        doc = items_collection.find_one({"Item_ID": item_id})
        if not doc:
            continue
        enriched.append({
            "iteminfo": {
                "item_id":   doc["Item_ID"],
                "item_name": doc["ItemName"],
                "type_item": doc["Type_Item"],
                "price":     str(doc["Price"]),
                "icon":      doc["Icon_Item"],
            }
        })

    # ── หาชุดล่าสุด +1 ───────────────────────────────────
    last = list(setitems_collection
                .find({"hero_name": hero_name})
                .sort("set", -1)
                .limit(1))
    next_set = (last[0]["set"] if last else 0) + 1

    # ── อัปเดต counters ─────────────────────────────────
    counters_collection.update_one(
        {"_id": f"set_{hero_name}"},
        {"$set": {"seq": next_set}},
        upsert=True
    )

    # ── Insert เอกสารชุดใหม่ ─────────────────────────────
    new_doc = {
        "set":       next_set,
        "hero_id":   hero_id,
        "hero_name": hero_name,
        "hero_icon": hero_icon,
        "items":     enriched,     # <-- ต้องใช้ enriched ไม่ใช่ global items
    }
    setitems_collection.insert_one(new_doc)

    return JSONResponse({"status": "ok", "set": next_set})

#--------------------- Setitems SETITEMS ROUTES --------------------
@app.get(
    "/setitems",
    response_model=List[dict],
    tags=["setitems"],
    summary="ดึงชุดไอเทมทั้งหมด",
    description="คืน JSON ของทุกชุดไอเทม"
)
def get_setitems():
    # 1) ดึงเอกสารทั้งหมด (ไม่เอา _id ของ MongoDB)
    docs = list(setitems_collection.find({}, {"_id": 0}))

    results = []
    for doc in docs:
        # 2) ดึงค่า "set" (จำนวนครั้งที่บันทึก) ออกมานำมาไว้หน้าสุด
        set_val = doc.pop("set", None)

        # 3) ถ้ามี field อื่นที่ไม่ต้องการ เช่น set_count ให้ลบทิ้ง
        doc.pop("set_count", None)

        # 4) สร้าง dict ใหม่: ให้ "set" มาอยู่บรรทัดแรก ตามด้วย field อื่นๆ
        reordered = {"set": set_val, **doc}
        results.append(reordered)

    # 5) คืนค่าเป็น JSON
    return jsonable_encoder(results)

    
#--------------------- Setitems_id SETITEMS ROUTES --------------------
@app.get(
    "/setitems/{hero_id}",
    response_model=List[dict],
    tags=["setitems"],
    summary="ดึงชุดไอเทมของฮีโร่",
    description="รับ hero_id → คืนชุดไอเทมทั้งหมดของฮีโร่นั้น"
)
def get_setitems_by_hero(hero_id: str):
    # ดึงข้อมูลจาก MongoDB (รวมฟิลด์ "set" ที่เราบันทึกไว้)
    docs = list(setitems_collection.find(
        {"hero_id": hero_id},
        {"_id": 0, "set": 1, "hero_id": 1, "hero_name": 1, "hero_icon": 1, "items": 1}
    ))
    results = []
    for doc in docs:
        # ดึงค่า set ออกมาก่อน (แล้วลบออกจาก dict หลัก)  
        set_val = doc.pop("set", None)
        # สร้าง dict ใหม่ ให้ "set" อยู่บรรทัดแรก
        reordered = {"set": set_val, **doc}
        results.append(reordered)
    # แปลงเป็น JSON-friendly แล้วคืนกลับไป
    return jsonable_encoder(results)



#---------------------- Delete_Set_Items ROUTES --------------------
@app.get("/delete_set_items", response_class=HTMLResponse,
        tags=["setitems"],
        summary="หน้า ลบชุดไอเทม",
        description="แสดงรายการชุดไอเทมทั้งหมด พร้อมปุ่ม Delete")
def page_delete_set_items(request: Request):
    sets = []
    for doc in setitems_collection.find().sort("set", 1):
        sets.append({
            "id": str(doc["_id"]),
            "set": doc.get("set"),
            "hero_id": doc.get("hero_id"),
            "hero_name": doc.get("hero_name"),
            "hero_icon": doc.get("hero_icon"),
        })
    return templates.TemplateResponse(
        "delete_set_items.html",
        {"request": request, "sets": sets}
    )

#----------------- API ลบชุดเดียว (delete one set) -------------------------------------
@app.delete("/delete_set_items/{doc_id}",
            tags=["setitems"],
            summary="ลบชุดไอเทม",
            description="ลบ document setitems ตาม ID ที่ส่งมา"
            )
def delete_set_items(doc_id: str):
    obj_id = ObjectId(doc_id)
    doc = setitems_collection.find_one({"_id": obj_id})
    if not doc:
        raise HTTPException(404, "Not Found")
    hero_name = doc["hero_name"]

    # ลบเอกสารชุดนั้น
    setitems_collection.delete_one({"_id": obj_id})
    # decrement counter ของฮีโร่คนนั้น ลง 1
    counters_collection.find_one_and_update(
        {"_id": f"set_{hero_name}"},
        {"$inc": {"seq": -1}},
        return_document=ReturnDocument.AFTER
    )

    return {"status": "deleted"}



#----------------- add_hero ROUTES --------------------
@app.get(
  "/add_heroes",
  response_class=HTMLResponse,
  tags=["heroes"],
  summary="หน้าเพิ่มฮีโร่ใหม่",
  description="แสดงฟอร์มอัปโหลดข้อมูลและรูปไอคอนฮีโร่"
)
def add_heroes_page(request: Request):
    return templates.TemplateResponse(
        "add_heroes.html",
        {"request": request}
    )
#------------------- add_hero POST ROUTES -------------------
def norm_str(v: Optional[str]) -> str:
    return v.strip() if v and v.strip() else "None"

def save_icon(file: Optional[UploadFile], prefix: str) -> Optional[str]:
    if not file or not file.filename:
        return None
    UP = "static/uploads"
    os.makedirs(UP, exist_ok=True)
    fn = f"{prefix}_{file.filename}"
    path = os.path.join(UP, fn)
    with open(path, "wb") as out:
        out.write(file.file.read())
    return f"/static/uploads/{fn}"

@app.post("/add_heroes", tags=["heroes"], summary="เพิ่มฮีโร่ใหม่")
async def add_hero(
    # ——— ฟิลด์ข้อความ ทุกตัว Optional[str] = Form(None) —————————————————
    hero_id:            Optional[str] = Form(None),
    hero_name:          Optional[str] = Form(None),
    role:               Optional[str] = Form(None),
    specialty:          Optional[str] = Form(None),
    lane_recc:          Optional[str] = Form(None),
    basic_attack_type:  Optional[str] = Form(None),
    price_battle_points:Optional[str] = Form(None),
    price_diamonds:     Optional[str] = Form(None),
    price_hero_fragments:Optional[str]= Form(None),
    price_tickets:      Optional[str] = Form(None),
    price_lucky_gem:    Optional[str] = Form(None),
    passive_name:       Optional[str] = Form(None),
    passive_detail:     Optional[str] = Form(None),
    skill_1_name:       Optional[str] = Form(None),
    skill_1_detail:     Optional[str] = Form(None),
    skill_2_name:       Optional[str] = Form(None),
    skill_2_detail:     Optional[str] = Form(None),
    skill_3_name:       Optional[str] = Form(None),
    skill_3_detail:     Optional[str] = Form(None),
    skill_4_name:       Optional[str] = Form(None),
    skill_4_detail:     Optional[str] = Form(None),
    swap_skill_1_name:  Optional[str] = Form(None),
    swap_skill_1_detail:Optional[str] = Form(None),
    swap_skill_2_name:  Optional[str] = Form(None),
    swap_skill_2_detail:Optional[str] = Form(None),
    swap_skill_3_name:  Optional[str] = Form(None),
    swap_skill_3_detail:Optional[str] = Form(None),
    durability:         Optional[str] = Form(None),
    offense:            Optional[str] = Form(None),
    control_effects:    Optional[str] = Form(None),
    difficulty:         Optional[str] = Form(None),
    hp:                 Optional[str] = Form(None),
    hp_regen:           Optional[str] = Form(None),
    armor_hp:           Optional[str] = Form(None),
    mana:               Optional[str] = Form(None),
    mana_regen:         Optional[str] = Form(None),
    energy:             Optional[str] = Form(None),
    energy_regen:       Optional[str] = Form(None),
    physical_attack:    Optional[str] = Form(None),
    magic_power:        Optional[str] = Form(None),
    physical_defense:   Optional[str] = Form(None),
    magic_defense:      Optional[str] = Form(None),
    attack_speed:       Optional[str] = Form(None),
    attack_speed_ratio: Optional[str] = Form(None),
    critical_chance:    Optional[str] = Form(None),
    critical_damage:    Optional[str] = Form(None),
    movement_speed:     Optional[str] = Form(None),
    basic_attack_range: Optional[str] = Form(None),

    # ——— รูป (Optional) ——————————————————————————————————
    iconhero:           Optional[UploadFile] = File(None),
    imagehero:          Optional[UploadFile] = File(None),
    passive_icon:       Optional[UploadFile] = File(None),
    skill_1_icon:       Optional[UploadFile] = File(None),
    skill_2_icon:       Optional[UploadFile] = File(None),
    skill_3_icon:       Optional[UploadFile] = File(None),
    skill_4_icon:       Optional[UploadFile] = File(None),
    swap_skill_1_icon:  Optional[UploadFile] = File(None),
    swap_skill_2_icon:  Optional[UploadFile] = File(None),
    swap_skill_3_icon:  Optional[UploadFile] = File(None),
):
    # ——— normalize ข้อความเป็น “None” เมื่อว่าง ——————————————————
    hero_id            = norm_str(hero_id)
    hero_name          = norm_str(hero_name)
    role               = norm_str(role)
    specialty          = norm_str(specialty)
    lane_recc          = norm_str(lane_recc)
    basic_attack_type  = norm_str(basic_attack_type)
    price_battle_points= norm_str(price_battle_points)
    price_diamonds     = norm_str(price_diamonds)
    price_hero_fragments=norm_str(price_hero_fragments)
    price_tickets      = norm_str(price_tickets)
    price_lucky_gem    = norm_str(price_lucky_gem)
    passive_name       = norm_str(passive_name)
    passive_detail     = norm_str(passive_detail)
    skill_1_name       = norm_str(skill_1_name)
    skill_1_detail     = norm_str(skill_1_detail)
    skill_2_name       = norm_str(skill_2_name)
    skill_2_detail     = norm_str(skill_2_detail)
    skill_3_name       = norm_str(skill_3_name)
    skill_3_detail     = norm_str(skill_3_detail)
    skill_4_name       = norm_str(skill_4_name)
    skill_4_detail     = norm_str(skill_4_detail)
    swap_skill_1_name  = norm_str(swap_skill_1_name)
    swap_skill_1_detail= norm_str(swap_skill_1_detail)
    swap_skill_2_name  = norm_str(swap_skill_2_name)
    swap_skill_2_detail= norm_str(swap_skill_2_detail)
    swap_skill_3_name  = norm_str(swap_skill_3_name)
    swap_skill_3_detail= norm_str(swap_skill_3_detail)
    durability         = norm_str(durability)
    offense            = norm_str(offense)
    control_effects    = norm_str(control_effects)
    difficulty         = norm_str(difficulty)
    hp                 = norm_str(hp)
    hp_regen           = norm_str(hp_regen)
    armor_hp           = norm_str(armor_hp)
    mana               = norm_str(mana)
    mana_regen         = norm_str(mana_regen)
    energy             = norm_str(energy)
    energy_regen       = norm_str(energy_regen)
    physical_attack    = norm_str(physical_attack)
    magic_power        = norm_str(magic_power)
    physical_defense   = norm_str(physical_defense)
    magic_defense      = norm_str(magic_defense)
    attack_speed       = norm_str(attack_speed)
    attack_speed_ratio = norm_str(attack_speed_ratio)
    critical_chance    = norm_str(critical_chance)
    critical_damage    = norm_str(critical_damage)
    movement_speed     = norm_str(movement_speed)
    basic_attack_range = norm_str(basic_attack_range)

    # ——— อัปโหลดไฟล์ (คืน URL หรือ None) ———————————————————
    iconhero_url     = save_icon(iconhero,      "iconhero")
    imagehero_url    = save_icon(imagehero,     "imagehero")
    passive_icon_url = save_icon(passive_icon,  "passive")
    skill1_icon_url  = save_icon(skill_1_icon,  "skill1")
    skill2_icon_url  = save_icon(skill_2_icon,  "skill2")
    skill3_icon_url  = save_icon(skill_3_icon,  "skill3")
    skill4_icon_url  = save_icon(skill_4_icon,  "skill4")
    swap1_icon_url   = save_icon(swap_skill_1_icon, "swap1")
    swap2_icon_url   = save_icon(swap_skill_2_icon, "swap2")
    swap3_icon_url   = save_icon(swap_skill_3_icon, "swap3")

    # ——— สร้างเอกสารและ insert ————————————————————————————————
    doc = {
        "Hero_ID":             hero_id or "None",
        "HeroName":            hero_name or "None",
        "Role":                role or "None",
        "Specialty":           specialty or "None",
        "Lane_Recc":           lane_recc or "None",
        "Basic_attack_type":   basic_attack_type or "None",

        "Price_Battle_Points": price_battle_points or "None",
        "Price_Diamonds":      price_diamonds or "None",
        "Price_hero_fragments":price_hero_fragments or "None",
        "Price_Tickets":       price_tickets or "None",
        "Price_lucky_gem":     price_lucky_gem or "None",

        "Iconhero":            iconhero_url or "None",
        "Imagehero":           imagehero_url or "None",

        "PassiveName":         passive_name or "None",
        "PassiveDetail":       passive_detail or "None",
        "Passive_icon":         passive_icon_url or "None",

        "Skill_1_Name":        skill_1_name or "None",
        "Skill_1_Detail":      skill_1_detail or "None",
        "Skill_1_icon":        skill1_icon_url or "None",

        "Skill_2_Name":        skill_2_name or "None",
        "Skill_2_Detail":      skill_2_detail or "None",
        "Skill_2_icon":        skill2_icon_url or "None",

        "Skill_3_Name":        skill_3_name or "None",
        "Skill_3_Detail":      skill_3_detail or "None",
        "Skill_3_icon":        skill3_icon_url or "None",

        "Skill_4_Name":        skill_4_name or "None",
        "Skill_4_Detail":      skill_4_detail or "None",
        "Skill_4_icon":        skill4_icon_url or "None",

        "Swap_Skill_1_Name":   swap_skill_1_name or "None",
        "Swap_Skill_1_Detail": swap_skill_1_detail or "None",
        "Swap_Skill_1_icon":   swap1_icon_url or "None",

        "Swap_Skill_2_Name":   swap_skill_2_name or "None",
        "Swap_Skill_2_Detail": swap_skill_2_detail or "None",
        "Swap_Skill_2_icon":   swap2_icon_url or "None",

        "Swap_Skill_3_Name":   swap_skill_3_name or "None",
        "Swap_Skill_3_Detail": swap_skill_3_detail or "None",
        "Swap_Skill_3_icon":   swap3_icon_url or "None",

        "Durability":          durability or "None",
        "Offense":             offense or "None",
        "Control_effects":     control_effects or "None",
        "Difficulty":          difficulty or "None",
        "HP":                  hp or "None",
        "HP_Regen":            hp_regen or "None",
        "Armor_HP":            armor_hp or "None",
        "Mana":                mana or "None",
        "Mana_Regen":          mana_regen or "None",
        "Energy":              energy or "None",
        "Energy_Regen":        energy_regen or "None",
        "Physical_Attack":     physical_attack or "None",
        "Magic_Power":         magic_power or "None",
        "Physical_Defense":    physical_defense or "None",
        "Magic_Defense":       magic_defense or "None",
        "Attack_Speed":        attack_speed or "None",
        "Attack_Speed_Ratio%": attack_speed_ratio or "None",
        "Critical_Chance%":    critical_chance or "None",
        "Critical_Damage%":    critical_damage or "None",
        "Movement_Speed":      movement_speed or "None",
        "Basic_Attack_Range":  basic_attack_range or "None",

    }
    heroes_collection.insert_one(doc)
    return JSONResponse({"status":"ok","hero_id":hero_id})