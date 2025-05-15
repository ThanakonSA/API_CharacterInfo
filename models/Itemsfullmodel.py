from pydantic import BaseModel

class ItemInfo(BaseModel):
    item_id:   str
    item_name: str
    type_item: str
    price:     str
    icon:      str

class ItemPassive(BaseModel):
    passive:   str

class ItemStats(BaseModel):
    physical_attack:   str
    magic_power:       str
    hp:                str
    hp_regen:          str
    mana:              str
    mana_regen:        str
    physical_defense:  str
    magic_defense:     str
    lifesteal:         str
    spell_vamp:        str
    hybrid_lifesteal:  str
    cooldown_reduction:str
    attack_speed:      str
    adaptive_attack:   str
    magic_penetration: str
    critical_chance:   str
    critical_damage:   str
    movement_speed:    str
    slow_reduction:    str

class ItemFullModel(BaseModel):
    iteminfo:  ItemInfo
    passive: ItemPassive
    stats: ItemStats

class ItemMainModel(BaseModel):
    iteminfo:  ItemInfo

    
def convert_row_to_item(row: dict) -> dict:
    return {
        "iteminfo": {
            "item_id":    row.get("Item_ID", ""),
            "item_name":  row.get("ItemName", ""),
            "type_item":  row.get("Type_Item", ""),
            "price":      row.get("Price", ""),
            "passive":    row.get("Passive", ""),
            "icon":       row.get("Icon_Item", ""),
            
        },
        "passive": {
            "passive":    row.get("Passive", ""),
        },
        "stats": {
            "physical_attack":    row.get("Physical_Attack", ""),
            "magic_power":        row.get("Magic_Power", ""),
            "hp":                 row.get("HP", ""),
            "hp_regen":           row.get("HP_Regen", ""),
            "mana":               row.get("Mana", ""),
            "mana_regen":         row.get("Mana_Regen", ""),
            "physical_defense":   row.get("Physical_Defense", ""),
            "magic_defense":      row.get("Magic_Defense", ""),
            "lifesteal":          row.get("Lifesteal", ""),
            "spell_vamp":         row.get("Spell_Vamp", ""),
            "hybrid_lifesteal":   row.get("Hybrid_Lifesteal", ""),
            "cooldown_reduction": row.get("Cooldown_Reduction", ""),
            "attack_speed":       row.get("Attack_Speed", ""),
            "adaptive_attack":    row.get("Adaptive_Attack", ""),
            "magic_penetration":  row.get("Magic_Penetration", ""),
            "critical_chance":    row.get("Critical_Chance", ""),
            "critical_damage":    row.get("Critical_Damage", ""),
            "movement_speed":     row.get("Movement_Speed", ""),
            "slow_reduction":     row.get("Slow_Reduction", ""),
        }
    }
