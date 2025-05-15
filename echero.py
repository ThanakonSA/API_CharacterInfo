import pandas as pd
from pymongo import MongoClient

file_path = "HeroInfo.xlsx"
df_main = pd.read_excel(file_path, sheet_name="Heroes")
df_icon = pd.read_excel(file_path, sheet_name="HeroesIcon")


df_main.columns = df_main.columns.str.strip()
df_icon.columns = df_icon.columns.str.strip()
df_main["Hero_ID"] = df_main["Hero_ID"].astype(str).str.strip().str.lower()
df_icon["Hero_ID"] = df_icon["Hero_ID"].astype(str).str.strip().str.lower()

df_merged = pd.merge(df_main, df_icon, on="Hero_ID", how="left")

df_clean = df_merged.where(pd.notnull(df_merged), None)

df_clean = df_clean.astype(str)

client = MongoClient("mongodb+srv://thanakon3:Teera0Chineseboi@cluster0.mft4otf.mongodb.net/")
db = client["MobileLegend_wiki_backend"]
collection = db["heroesinfos"]
collection.delete_many({})
collection.insert_many(df_clean.to_dict(orient="records"))

print("อัปโหลดฮีโร่เสร็จเรียบร้อย")