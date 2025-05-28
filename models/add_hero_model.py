from pydantic import BaseModel, Field
from fastapi import Form

class HeroForm(BaseModel):
    Hero_ID: str = Field(..., description="รหัสฮีโร่")
    HeroName: str = Field(..., description="ชื่อฮีโร่")
    Role: str = ""
    Specialty: str = ""
    Lane_Recc: str = ""
    Basic_attack_type: str = ""

    Price_Battle_Points: str = ""
    Price_Diamons: str = ""
    Price_hero_fragments: str = ""
    Price_Tickets: str = ""
    Price_lucky_gem: str = ""

    PassiveName: str = ""
    PassiveDetail: str = ""

    Skill_1_Name: str = ""
    Skill_1_Detail: str = ""
    Skill_2_Name: str = ""
    Skill_2_Detail: str = ""
    Skill_3_Name: str = ""
    Skill_3_Detail: str = ""
    Skill_4_Name: str = ""
    Skill_4_Detail: str = ""

    Swap_Skill_1_Name: str = ""
    Swap_Skill_1_Detail: str = ""
    Swap_Skill_2_Name: str = ""
    Swap_Skill_2_Detail: str = ""
    Swap_Skill_3_Name: str = ""
    Swap_Skill_3_Detail: str = ""

    Durability: str = ""
    Offense: str = ""
    Control_effects: str = ""
    Difficulty: str = ""

    HP: str = ""
    HP_Regen: str = ""
    Armor_HP: str = ""
    Mana: str = ""
    Mana_Regen: str = ""
    Energy: str = ""
    Energy_Regen: str = ""

    Physical_Attack: str = ""
    Magic_Power: str = ""
    Physical_Defense: str = ""
    Magic_Defense: str = ""
    Attack_Speed: str = ""
    Attack_Speed_Ratio: str = Field("", alias="Attack_Speed_Ratio%")
    Critical_Chance: str = Field("", alias="Critical_Chance%")
    Critical_Damage: str = Field("", alias="Critical_Damage%")
    Movement_Speed: str = ""
    Basic_Attack_Range: str = ""


def get_hero_form(
    Hero_ID: str = Form(...),
    HeroName: str = Form(...),
    Role: str = Form(""),
    Specialty: str = Form(""),
    Lane_Recc: str = Form(""),
    Basic_attack_type: str = Form(""),
    Price_Battle_Points: str = Form(""),
    Price_Diamonds: str = Form(""),
    Price_hero_fragments: str = Form(""),
    Price_Tickets: str = Form(""),
    Price_lucky_gem: str = Form(""),
    PassiveName: str = Form(""),
    PassiveDetail: str = Form(""),
    Skill_1_Name: str = Form(""),
    Skill_1_Detail: str = Form(""),
    Skill_2_Name: str = Form(""),
    Skill_2_Detail: str = Form(""),
    Skill_3_Name: str = Form(""),
    Skill_3_Detail: str = Form(""),
    Skill_4_Name: str = Form(""),
    Skill_4_Detail: str = Form(""),
    Swap_Skill_1_Name: str = Form(""),
    Swap_Skill_1_Detail: str = Form(""),
    Swap_Skill_2_Name: str = Form(""),
    Swap_Skill_2_Detail: str = Form(""),
    Swap_Skill_3_Name: str = Form(""),
    Swap_Skill_3_Detail: str = Form(""),
    Durability: str = Form(""),
    Offense: str = Form(""),
    Control_effects: str = Form(""),
    Difficulty: str = Form(""),
    HP: str = Form(""),
    HP_Regen: str = Form(""),
    Armor_HP: str = Form(""),
    Mana: str = Form(""),
    Mana_Regen: str = Form(""),
    Energy: str = Form(""),
    Energy_Regen: str = Form(""),
    Physical_Attack: str = Form(""),
    Magic_Power: str = Form(""),
    Physical_Defense: str = Form(""),
    Magic_Defense: str = Form(""),
    Attack_Speed: str = Form(""),
    Attack_Speed_Ratio: str = Form(""),
    Critical_Chance: str = Form(""),
    Critical_Damage: str = Form(""),
    Movement_Speed: str = Form(""),
    Basic_Attack_Range: str = Form(""),
) -> HeroForm:
    # alias_fields ต้อง map ชื่อที่มี % ให้ตรงกับ model
    data = {
      **locals(),
      "Attack_Speed_Ratio%": locals()["Attack_Speed_Ratio"],
      "Critical_Chance%": locals()["Critical_Chance"],
      "Critical_Damage%": locals()["Critical_Damage"],
    }
    return HeroForm.parse_obj(data)