from pydantic import BaseModel
from typing import Optional

# โมเดลสำหรับข้อมูลบางส่วนของฮีโร่
class HeroDetailModel(BaseModel):
    Hero_ID: str
    HeroName: str
    Role: Optional[str] = None
    Specialty: Optional[str] = None
    Lane_Recc: Optional[str] = None
    Durability: Optional[str] = None
    Offense: Optional[str] = None
    Control_effects: Optional[str] = None
    Difficulty: Optional[str] = None
    Passive: Optional[str] = None
    Skill_1: Optional[str] = None
    Skill_2: Optional[str] = None
    Skill_3: Optional[str] = None
    Price_Battle_Points: Optional[str] = None
    Price_Diamons: Optional[str] = None
    HP: Optional[str] = None
    HP_Regen: Optional[str] = None
    Mana: Optional[str] = None
    Mana_Regen: Optional[str] = None
    Physical_Attack: Optional[str] = None
    Magic_Power: Optional[str] = None
    Physical_Defense: Optional[str] = None
    Magic_Defense: Optional[str] = None
    Attack_Speed: Optional[str] = None
    Attack_Speed_Ratio: Optional[str] = None
    Critical_Damage: Optional[str] = None
    Movement_Speed: Optional[str] = None
    Basic_Attack_Range: Optional[str] = None
    Iconhero: Optional[str] = None
    Imagehero: Optional[str] = None
    Passive_icon: Optional[str] = None
    Skill_1_icon: Optional[str] = None
    Skill_2_icon: Optional[str] = None
    Skill_3_icon: Optional[str] = None