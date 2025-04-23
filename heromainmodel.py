from pydantic import BaseModel
from typing import Optional

# โมเดลสำหรับข้อมูลบางส่วนของฮีโร่
class HeroMainModel(BaseModel):
    Hero_ID: str
    HeroName: str
    Role: Optional[str] = None
    Lane_Recc: Optional[str] = None
    Iconhero: Optional[str] = None