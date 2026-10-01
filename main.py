import sqlite3
import os

# Database path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "foods.db")

def init_db():
    """Creates the table and seeds it if empty."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            region TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    
    # Check if empty
    cur.execute("SELECT COUNT(*) FROM foods")
    if cur.fetchone()[0] == 0:
        print("🌱 Seeding initial data...")
        sample_data = [
            ("Nyama Choma", "Central Kenya", "Beef, Salt, Charcoal", 1200),
            ("Mukimo", "Central Kenya", "Maize, Beans, Potatoes, Pumpkin leaves", 250),
            ("Pilau", "Coast", "Rice, Beef, Pilau Masala", 450),
            ("Mutura", "Central Kenya", "Minced meat, Tripe, Blood, Spices", 100)
        ]
        cur.executemany("INSERT INTO foods (name, region, ingredients, price) VALUES (?, ?, ?, ?)", sample_data)
        conn.commit()
    
    conn.close()

def suggest_food():
    """Picks one random food."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, region, ingredients, price FROM foods ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()
    return row

def get_foods_by_region(region_name):
    """Returns all foods belonging to a specific region."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT name, ingredients, price 
        FROM foods 
        WHERE region = ?
    """, (region_name,))
    rows = cur.fetchall()
    conn.close()
    return rows

def print_suggestion(food):
    if not food:
        print("\n⚠️ No food data found.")
        return
    name, region, ingredients, price = food
    print("\n" + "═"*35)
    print(f" 🍴 TODAY'S PICK: {name}")
    print(f" Region: {region} | Price: KES {price:.0f}")
    print(f" Ingredients: {ingredients}")
    print("═"*35)

def show_all_regions():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT region, COUNT(*) FROM foods GROUP BY region ORDER BY 2 DESC")
    rows = cur.fetchall()
    conn.close()
    print("\n📊 Current Stats:")
    for region, cnt in rows:
        print(f"  {region:<15} {'█' * cnt} ({cnt})")

if __name__ == "__main__":
    init_db()
    
    # 1. Show the stats chart
    show_all_regions()
    
    # 2. Get a random suggestion
    random_pick = suggest_food()
    print_suggestion(random_pick)
    
    # 3. Filtered Search (The part you requested)
    target_region = "Central Kenya"
    print(f"\n🔍 Searching all foods in: {target_region}")
    regional_foods = get_foods_by_region(target_region)
    
    if regional_foods:
        for item in regional_foods:
            name, ingr, price = item
            print(f"  • {name:<12} | KES {price:>4.0f} | Ingredients: {ingr}")
    else:
        print(f"  No foods found for {target_region}")