from pydantic import BaseModel, Field

class HeroBase(BaseModel):
    hero_id: str
    hero_name: str
    role: str
    specialty: str
    lane_recc: str
    icon: str
    full: str

class HeroPrice(BaseModel):
    battle_points: str
    diamonds: str
    hero_fragments: str
    tickets: str
    lucky_gem: str

class SkillDetail(BaseModel):
    name: str
    detail: str
    icon: str

class HeroSkills(BaseModel):
    passive: SkillDetail
    skill_1: SkillDetail
    skill_2: SkillDetail
    skill_3: SkillDetail
    skill_4: SkillDetail
    swap_skill_1: SkillDetail
    swap_skill_2: SkillDetail
    swap_skill_3: SkillDetail

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
    energy: str
    energy_regen: str
    armor_hp: str
    physical_defense: str
    magic_defense: str
    physical_attack: str
    magic_power: str
    attack_speed: str
    attack_speed_ratio:  str
    critical_chance:     str
    critical_damage:     str
    movement_speed: str
    basic_attack_type: str
    basic_attack_range: str


class HeroFullModel(BaseModel):
    herobase: HeroBase
    price: HeroPrice
    skills: HeroSkills
    ratings: HeroRatings
    stats: HeroStats


def convert_row_to_heroes(row: dict) -> dict:
    return {
        "herobase": {
            "hero_id":   row.get("Hero_ID", ""),
            "hero_name": row.get("HeroName", ""),
            "role":      row.get("Role", ""),
            "specialty": row.get("Specialty", ""),
            "lane_recc": row.get("Lane_Recc", ""),
            "icon":      row.get("Iconhero", ""),
            "full":      row.get("Imagehero", "")
        },
        "price": {
            "battle_points":  row.get("Price_Battle_Points", ""),
            "diamonds":       row.get("Price_Diamons", ""),
            "hero_fragments": row.get("Price_hero_fragments", ""),
            "tickets":        row.get("Price_Tickets", ""),
            "lucky_gem":      row.get("Price_lucky_gem", ""),
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
            "skill_4": {
                "name":   row.get("Skill_4_Name", ""),
                "detail": row.get("Skill_4_Detail", ""),
                "icon":   row.get("Skill_4_icon", "")
            },
            "swap_skill_1": {
                "name":   row.get("Swap_Skill_1_Name", ""),
                "detail": row.get("Swap_Skill_1_Detail", ""),
                "icon":   row.get("Swap_Skill_1_icon", "")
            },
            "swap_skill_2": {
                "name":   row.get("Swap_Skill_2_Name", ""),
                "detail": row.get("Swap_Skill_2_Detail", ""),
                "icon":   row.get("Swap_Skill_2_icon", "")
            },
            "swap_skill_3": {
                "name":   row.get("Swap_Skill_3_Name", ""),
                "detail": row.get("Swap_Skill_3_Detail", ""),
                "icon":   row.get("Swap_Skill_3_icon", "")
            },
        },
        "ratings": {
            "durability":      row.get("Durability", ""),
            "offense":         row.get("Offense", ""),
            "control_effects": row.get("Control_effects", ""),
            "difficulty":      row.get("Difficulty", ""),
        },
        "stats": {
            "hp":                  row.get("HP", ""),
            "hp_regen":            row.get("HP_Regen", ""),
            "mana":                row.get("Mana", ""),
            "mana_regen":          row.get("Mana_Regen", ""),
            "energy":              row.get("Energy", ""),
            "energy_regen":        row.get("Energy_Regen", ""),
            "armor_hp":            row.get("Armor_HP", ""),
            "physical_defense":    row.get("Physical_Defense", ""),
            "magic_defense":       row.get("Magic_Defense", ""),
            "physical_attack":     row.get("Physical_Attack", ""),
            "magic_power":         row.get("Magic_Power", ""),
            "attack_speed":        row.get("Attack_Speed", ""),
            "attack_speed_ratio": row.get("Attack_Speed_Ratio%", ""),
            "critical_chance":     row.get("Critical_Chance%", ""),
            "critical_damage":     row.get("Critical_Damage%", ""),
            "movement_speed":      row.get("Movement_Speed", ""),
            "basic_attack_type":   row.get("Basic_attack_type", ""),
            "basic_attack_range":  row.get("Basic_Attack_Range", ""),
        }
    }
