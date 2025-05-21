from pydantic import BaseModel
from typing import List

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
    lifesteal_:         str
    spell_vamp_:        str
    hybrid_lifesteal_:  str
    cooldown_reduction_:str
    attack_speed_:      str
    adaptive_attack:   str
    adaptive_attack_:   str
    physical_penetration: str
    physical_penetration_:str
    magic_penetration: str 
    magic_penetration_:str
    critical_chance_:   str
    critical_damage_:   str
    movement_speed:    str
    movement_speed_:    str
    slow_reduction_:    str
    healing_effect_:   str

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
            "physical_attack":              row.get("Physical_Attack", ""),
            "magic_power":                  row.get("Magic_Power", ""),
            "hp":                           row.get("HP", ""),
            "hp_regen":                     row.get("HP_Regen", ""),
            "mana":                         row.get("Mana", ""),
            "mana_regen":                   row.get("Mana_Regen", ""),
            "physical_defense":             row.get("Physical_Defense", ""),
            "magic_defense":                row.get("Magic_Defense", ""),
            "lifesteal_":                   row.get("Lifesteal%", ""),
            "spell_vamp_":                  row.get("Spell_Vamp%", ""),
            "hybrid_lifesteal_":            row.get("Hybrid_Lifesteal%", ""),
            "cooldown_reduction_":          row.get("Cooldown_Reduction%", ""),
            "attack_speed_":                row.get("Attack_Speed%", ""),
            "adaptive_attack":              row.get("Adaptive_Attack", ""),
            "adaptive_attack_":             row.get("Adaptive_Attack%", ""),
            "physical_penetration":         row.get("Physical_Penetration", ""),
            "physical_penetration_":        row.get("Physical_Penetration%", ""),
            "magic_penetration":            row.get("Magic_Penetration", ""),
            "magic_penetration_":           row.get("Magic_Penetration%", ""),
            "critical_chance_":             row.get("Critical_Chance%", ""),
            "critical_damage_":             row.get("Critical_Damage%", ""),
            "critical_damage_reduction_":   row.get("Critical_Damage_Reduction%", ""),
            "movement_speed":               row.get("Movement_Speed", ""),
            "movement_speed_":              row.get("Movement_Speed%", ""),
            "slow_reduction_":              row.get("Slow_Reduction%", ""),
            "healing_effect_":              row.get("Healing_Effect%", ""),
        }
    }
