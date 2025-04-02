from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient("mongodb+srv://thanakon3:Teera0Chineseboi@cluster0.mft4otf.mongodb.net/")
db = client["MobileLegend_wiki_backend"]
collection = db["characterinfos"]

def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.get("/heroes")
def get_all_heroes():
    heroes = list(collection.find())
    return [fix_id(hero) for hero in heroes]

@app.get("/heroes/name/{name}")
def get_hero_by_name(name: str):
    hero = collection.find_one({"HeroName": name})
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return fix_id(hero)

@app.get("/heroes/type/{type_name}")
def get_heroes_by_type(type_name: str):
    heroes = list(collection.find({"Type": type_name}))
    if not heroes:
        raise HTTPException(status_code=404, detail=f"No heroes found in type: {type_name}")
    return [fix_id(hero) for hero in heroes]





