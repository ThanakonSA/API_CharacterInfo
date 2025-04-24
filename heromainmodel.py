from pydantic import BaseModel
from typing import Optional

class HeroBase(BaseModel):
    hero_id: str
    hero_name: str
    role: str
    lane_recc: str
    icon: str

class HeroMainModel(BaseModel):
    herobase: HeroBase


def convert_row_to_heroesmain(row: dict) -> dict:
    return {
        "herobase": {
            "hero_id":    row.get("Hero_ID", ""),
            "hero_name":  row.get("HeroName", ""),
            "role":       row.get("Role", ""),
            "lane_recc":  row.get("Lane_Recc", ""),
            "icon":       row.get("Iconhero", ""),
            }
    }
