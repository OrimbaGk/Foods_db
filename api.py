from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "foods.db")

def query_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def execute_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()

class AddRegionsRequest(BaseModel):
    new_regions: List[str]

@app.get("/")
def home():
    return {"message": "Foods API running"}

@app.get("/foods")
def get_all_foods():
    rows = query_db("SELECT * FROM foods")
    return rows

@app.get("/foods/region/{region}")
def foods_by_region(region: str):
    rows = query_db(
        "SELECT name, ingredients, price FROM foods WHERE region = ?",
        (region,)
    )
    return rows

@app.get("/foods/search/{keyword}")
def search_foods(keyword: str):
    rows = query_db(
        "SELECT name, region, price FROM foods WHERE name LIKE ?",
        ('%' + keyword + '%',)
    )
    return rows

@app.get("/foods/regions")
def get_all_regions():
    rows = query_db("SELECT DISTINCT region FROM foods")
    return [r[0] for r in rows]

@app.post("/add-regions")
def add_regions(body: AddRegionsRequest):
    if not body.new_regions:
        raise HTTPException(status_code=400, detail="new_regions list cannot be empty")

    existing = [r[0] for r in query_db("SELECT DISTINCT region FROM foods")]
    added = []
    skipped = []

    for region in body.new_regions:
        region = region.strip()
        if region in existing:
            skipped.append(region)
        else:
            execute_db(
                "INSERT INTO foods (name, region, ingredients, price) VALUES (?, ?, ?, ?)",
                (f"Sample dish ({region})", region, "To be updated", 0.00)
            )
            added.append(region)

    return {
        "message": "Done",
        "added": added,
        "skipped_already_exist": skipped
    }
@app.post("/foods")
def add_food(food: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO foods (name, region, ingredients, price)
        VALUES (?, ?, ?, ?)
    """, (
        food["name"],
        food["region"],
        food["ingredients"],
        food["price"]
    ))

    conn.commit()
    conn.close()

    return {"message": "Food added successfully"}