import csv
import sqlite3
import os

def clean_and_load(raw_csv="raw_villages.csv", db_file="../backend/database.sqlite"):
    raw_path = os.path.join(os.path.dirname(__file__), raw_csv)
    db_path = os.path.join(os.path.dirname(__file__), db_file)
    
    # Ensure backend directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS villages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state TEXT,
            district TEXT,
            sub_district TEXT,
            village_name TEXT,
            population INTEGER,
            area_hectares REAL,
            literacy_rate REAL
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM villages')
    
    cleaned_rows = []
    
    print("Reading and cleaning data...")
    with open(raw_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Data Cleaning Logic
            
            # 1. Fill missing population with average or median (here just a default of 500 for simplicity)
            population = row['Population']
            if not population or not population.strip():
                population = 500
            else:
                population = int(population)
                
            # 2. Fill missing literacy rate with a default of 50.0
            literacy = row['Literacy_Rate']
            if not literacy or not literacy.strip():
                literacy = 50.0
            else:
                literacy = float(literacy)
                
            area = float(row['Area_Hectares'])
            
            cleaned_rows.append((
                row['State'],
                row['District'],
                row['SubDistrict'],
                row['VillageName'],
                population,
                area,
                literacy
            ))
            
    print(f"Cleaned {len(cleaned_rows)} rows. Inserting into database...")
    
    cursor.executemany('''
        INSERT INTO villages (state, district, sub_district, village_name, population, area_hectares, literacy_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', cleaned_rows)
    
    # Create indexes for faster search
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_state ON villages(state)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_district ON villages(district)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_village_name ON villages(village_name)')
    
    conn.commit()
    conn.close()
    
    print(f"Data successfully loaded into {db_path}")

if __name__ == "__main__":
    clean_and_load()
