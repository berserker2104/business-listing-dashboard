import mysql.connector
from faker import Faker
import random

fake = Faker('en_IN')  
CATEGORIES = [
    "Restaurant", "Hospital", "Gym", "Hotel", "Salon",
    "Electronics", "Pharmacy", "Coaching Center", "Real Estate", "Grocery Store"
]

CITIES = [
    "Mumbai", "Pune", "Delhi", "Bangalore", "Chennai",
    "Hyderabad", "Ahmedabad", "Surat", "Jaipur", "Kolkata"
]

SOURCES = ["Justdial", "Sulekha", "Google Maps", "IndiaMart", "Yellowpages"]

NAME_PREFIXES = {
    "Restaurant":       ["Spice Garden", "Royal Dhaba", "Tandoor House", "Mumbai Bites", "Curry Leaf"],
    "Hospital":         ["Life Care", "Apollo", "Sunrise", "Healing Touch", "City Medical"],
    "Gym":              ["FitZone", "PowerHouse", "Iron Body", "Peak Fitness", "Gold's"],
    "Hotel":            ["Grand Stay", "Comfort Inn", "Royal Residency", "Star Lodge", "Elite Suites"],
    "Salon":            ["Style Studio", "Glamour Zone", "The Hair Lounge", "Beauty Hub", "Scissors & Co"],
    "Electronics":      ["TechMart", "Gadget World", "Digital Zone", "SmartShop", "Circuit Hub"],
    "Pharmacy":         ["LifeLine Pharmacy", "MedPlus", "HealthFirst", "CurePlus", "Apollo Pharmacy"],
    "Coaching Center":  ["Bright Future", "Success Point", "EduVision", "TopRank", "Knowledge Hub"],
    "Real Estate":      ["PropDeal", "HomeBase", "Realty Plus", "DreamHome", "BuildRight"],
    "Grocery Store":    ["FreshMart", "Daily Needs", "Kirana Store", "SuperBazaar", "Nature's Basket"]
}

AREA_SUFFIXES = [
    "Nagar", "Vihar", "Colony", "Sector", "Road",
    "Chowk", "Market", "Park", "Layout", "Extension"
]


def generate_phone():
    """Generate realistic Indian mobile number"""
    prefixes = ["98", "97", "96", "95", "90", "89", "88", "87", "86", "70"]
    return "+91 " + random.choice(prefixes) + str(random.randint(10000000, 99999999))


def generate_address(city):
    """Generate realistic Indian address"""
    num = random.randint(1, 999)
    area = fake.last_name() + " " + random.choice(AREA_SUFFIXES)
    return f"{num}, {area}, {city} - {random.randint(400001, 500099)}"


def generate_listings(n=550):
    listings = []
    for _ in range(n):
        category = random.choice(CATEGORIES)
        city = random.choice(CITIES)
        prefix = random.choice(NAME_PREFIXES[category])
        suffix = fake.last_name()
        business_name = f"{prefix} {suffix}"

        listings.append({
            "business_name": business_name,
            "category": category,
            "city": city,
            "address": generate_address(city),
            "phone": generate_phone(),
            "source": random.choice(SOURCES),
        })
    return listings

def insert_into_db(listings):
    conn = None     
    cursor = None

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sdk21000",  
            database="business_Dashboard"
        )
        cursor = conn.cursor()

        sql = """
            INSERT INTO listing_master 
                (business_name, category, city, address, phone, source)
            VALUES 
                (%s, %s, %s, %s, %s, %s)
        """

        batch = [
            (
                l["business_name"], l["category"], l["city"],
                l["address"], l["phone"], l["source"]
            )
            for l in listings
        ]

        cursor.executemany(sql, batch)
        conn.commit()
        print(f"✅ Successfully inserted {cursor.rowcount} records.")

    except mysql.connector.Error as e:
        print(f" MySQL Error: {e}")

    finally:
        if cursor is not None:   # ← only close if it was created
            cursor.close()
        if conn is not None:     # ← only close if it was created
            conn.close()


def verify_data():
    """Quick check — prints counts after insert"""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sdk21000", 
        database="business_Dashboard"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM listing_master")
    total = cursor.fetchone()[0]
    print(f"\n📊 Total records: {total}")

    cursor.execute("SELECT city, COUNT(*) as cnt FROM listing_master GROUP BY city ORDER BY cnt DESC")
    print("\n  City-wise count:")
    for row in cursor.fetchall():
        print(f"   {row[0]:<15} → {row[1]}")

    cursor.execute("SELECT source, COUNT(*) as cnt FROM listing_master GROUP BY source ORDER BY cnt DESC")
    print("\n Source-wise count:")
    for row in cursor.fetchall():
        print(f"   {row[0]:<15} → {row[1]}")

    cursor=None
    conn= None


if __name__ == "__main__":
    print(" Generating 550 business listings...")
    data = generate_listings(550)

    print(" Inserting into MySQL...")
    insert_into_db(data)

    print("\n Verifying data...")
    verify_data()