from pydantic import BaseModel
from typing import List, Optional
from .Itemsfullmodel import ItemFullModel, ItemMainModel


class CreateItemBuild(BaseModel):
    hero_id: str
    item_ids: List[str]         # รายการ Item_ID ที่ต้องการใส่ (length = 6)

class ItemBuild(BaseModel):
    setitems_id:    int            # รหัสชุดที่อัตโนมัติเพิ่มทีละ 1
    hero_id:        str
    items:          List[ItemMainModel] 

class PatchItemBuild(BaseModel):
    hero_id:      Optional[str]                 = None
    item_ids:     Optional[List[Optional[str]]] = None  # ถ้าใส่ ก็ต้องมี length=6

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