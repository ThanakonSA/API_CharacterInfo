from pydantic import BaseModel

class HeroMainModel(BaseModel):
    hero_id: str
    hero_name: str
    role: str
    specialty: str
    lane_recc: str
    icon: str
    full: str
    
# class HeroBase(BaseModel):
#     hero_id: str
#     hero_name: str
#     role: str
#     specialty: str
#     lane_recc: str
#     icon: str
#     full: str

# class HeroMainModel(BaseModel):
#     herobase: HeroBase


# def convert_row_to_heroesmain(row: dict) -> dict:
#     return {
#         "herobase": {
#             "hero_id":    row.get("Hero_ID", ""),
#             "hero_name":  row.get("HeroName", ""),
#             "role":       row.get("Role", ""),
#             "specialty":  row.get("Specialty", ""),
#             "lane_recc":  row.get("Lane_Recc", ""),
#             "icon":       row.get("Iconhero", ""),
#             "full":       row.get("Imagehero", "")
#             }
#     }