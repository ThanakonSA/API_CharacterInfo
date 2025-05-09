from pydantic import BaseModel
from typing import Optional

class HeroBase(BaseModel):
    hero_id: str
    hero_name: str
    role: str
    specialty: str
    lane_recc: str

class HeroPrice(BaseModel):
    battle_points: str
    diamonds: str

class SkillDetail(BaseModel):
    name: str
    detail: str
    icon: str

class HeroSkills(BaseModel):
    passive: SkillDetail
    skill_1: SkillDetail
    skill_2: SkillDetail
    skill_3: SkillDetail

class HeroRatings(BaseModel):
    durability: str
    offense: str
    control_effects: str
    difficulty: str

class HeroStats(BaseModel):
    hp: str
    hp_regen: str
    mana: str
    mana_regen: str
    physical_attack: str
    magic_power: str
    physical_defense: str
    magic_defense: str
    attack_speed: str
    attack_speed_ratio: str
    critical_damage: str
    movement_speed: str
    basic_attack_range: str

class HeroImages(BaseModel):
    icon: str
    full: str

class HeroDetailModel(BaseModel):
    herobase: HeroBase
    price:    HeroPrice
    ratings:  HeroRatings
    skills:   HeroSkills
    stats:    HeroStats
    images:   HeroImages


def convert_row_to_heroesdetail(row: dict) -> dict:
    return {
        "herobase": {
            "hero_id":    row.get("Hero_ID", ""),
            "hero_name":  row.get("HeroName", ""),
            "role":       row.get("Role", ""),
            "specialty":  row.get("Specialty", ""),
            "lane_recc":  row.get("Lane_Recc", ""),
        },
        "price": {
            "battle_points": row.get("Price_Battle_Points", ""),
            "diamonds":      row.get("Price_Diamonds", ""), 
        },
        "ratings": {
            "durability":      row.get("Durability", ""),
            "offense":         row.get("Offense", ""),
            "control_effects": row.get("Control_effects", ""),
            "difficulty":      row.get("Difficulty", ""),
        },
        "skills": {
            "passive": {
                "name":   row.get("PassiveName", ""),
                "detail": row.get("PassiveDetail", ""),
                "icon":   row.get("Passive_icon", "")
            },
            "skill_1": {
                "name":   row.get("Skill_1_Name", ""),
                "detail": row.get("Skill_1_Detail", ""),
                "icon":   row.get("Skill_1_icon", "")
            },
            "skill_2": {
                "name":   row.get("Skill_2_Name", ""),
                "detail": row.get("Skill_2_Detail", ""),
                "icon":   row.get("Skill_2_icon", "")
            },
            "skill_3": {
                "name":   row.get("Skill_3_Name", ""),
                "detail": row.get("Skill_3_Detail", ""),
                "icon":   row.get("Skill_3_icon", "")
            },
        },
        "stats": {
            "hp":                  row.get("HP", ""),
            "hp_regen":            row.get("HP_Regen", ""),
            "mana":                row.get("Mana", ""),
            "mana_regen":          row.get("Mana_Regen", ""),
            "physical_attack":     row.get("Physical_Attack", ""),
            "magic_power":         row.get("Magic_Power", ""),
            "physical_defense":    row.get("Physical_Defense", ""),
            "magic_defense":       row.get("Magic_Defense", ""),
            "attack_speed":        row.get("Attack_Speed", ""),
            "attack_speed_ratio":  row.get("Attack_Speed_Ratio", ""),
            "critical_damage":     row.get("Critical_Damage", ""),
            "movement_speed":      row.get("Movement_Speed", ""),
            "basic_attack_range":  row.get("Basic_Attack_Range", ""),
        },
        "images": {
            "icon": row.get("Iconhero", ""),
            "full": row.get("Imagehero", "")
        }
    }
