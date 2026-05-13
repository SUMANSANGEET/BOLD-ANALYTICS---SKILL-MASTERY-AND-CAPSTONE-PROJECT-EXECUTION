import csv
import random
import os

# Sample constants for mock data generation
STATES = ["Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan", "Uttar Pradesh", "Bihar", "West Bengal", "Punjab", "Haryana"]

DISTRICTS_BY_STATE = {
    "Maharashtra": ["Pune", "Mumbai", "Nagpur", "Nashik", "Thane"],
    "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia"],
    "West Bengal": ["Kolkata", "Darjeeling", "Howrah", "Siliguri", "Durgapur"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
    "Haryana": ["Faridabad", "Gurugram", "Panipat", "Ambala", "Rohtak"]
}

VILLAGE_PREFIXES = ["Nava", "Kala", "Badi", "Chhoti", "Lal", "Moti", "Hari", "Naya", "Pura"]
VILLAGE_SUFFIXES = ["pur", "garh", "nagar", "wadi", "gaon", "khurd", "kalan", "peta", "halli"]

def generate_village_name():
    if random.random() > 0.5:
        return f"{random.choice(VILLAGE_PREFIXES)}{random.choice(VILLAGE_SUFFIXES)}"
    else:
        return f"{random.choice(VILLAGE_PREFIXES)} {random.choice(VILLAGE_SUFFIXES).capitalize()}"

def generate_dataset(num_rows=10000, filename="raw_villages.csv"):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["State", "District", "SubDistrict", "VillageName", "Population", "Area_Hectares", "Literacy_Rate"])
        
        for i in range(num_rows):
            state = random.choice(STATES)
            district = random.choice(DISTRICTS_BY_STATE[state])
            sub_district = f"{district} Taluka"
            village_name = generate_village_name()
            # Randomize demographics
            population = random.randint(100, 15000)
            area = round(random.uniform(50.0, 5000.0), 2)
            literacy = round(random.uniform(40.0, 95.0), 2)
            
            # Occasionally add some dirty data (nulls) to simulate real-world cleaning requirement
            if random.random() < 0.05:
                population = ""
            if random.random() < 0.05:
                literacy = ""
                
            writer.writerow([state, district, sub_district, f"{village_name} {i}", population, area, literacy])
    
    print(f"Generated {num_rows} raw records in {filepath}")

if __name__ == "__main__":
    generate_dataset()
