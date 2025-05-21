from pydantic import BaseModel
from typing import List, Optional
from .Itemsfullmodel import ItemMainModel


class CreateItemBuild(BaseModel):
    hero_id: str
    hero_name:    str
    item_ids: List[str]       # รายการ Item_ID ที่ต้องการใส่ (length = 6)

class PatchItemBuild(BaseModel):
    hero_id:      Optional[str]                 = None
    item_ids:     Optional[List[Optional[str]]] = None  # ถ้าใส่ ก็ต้องมี length=6


class ItemBuild(BaseModel):
    hero_id:   str
    hero_name: str
    items:     List[ItemMainModel]

    class Config:
        schema_extra = {
            "example": {
                "hero_id":   "10256762575679",
                "hero_name": "Layla",
                "items": [
                    {"iteminfo": {"item_id":"31257721400913","item_name":"Windtalker","type_item":"Attack","price":"1880 GOLD","icon":"…"}},
                    {"iteminfo": {"item_id":"31258704040819","item_name":"Berserker's Fury","type_item":"Attack","price":"2390 GOLD","icon":"…"}},
                    ...
                ]
            }
        }

    class Config:
        json_schema_extra = {
            "example": {
                # ตัวอย่างข้อมูล (static) เพื่อให้ Swagger UI แสดงเป็น placeholder
                "hero_id": "Hero ID",
                "item_ids": [
                    "Item ID",
                    None,
                    None,
                    None,
                    None,
                    None
                ]
            }
        }