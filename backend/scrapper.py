"""
⚠️ WARNING - DO NOT RUN THIS FILE
-----------------------------------
This script was an attempt to scrape live business listings
from Justdial. The scraping was blocked due to:
- CAPTCHA protection
- IP rate limiting
- Dynamic JavaScript rendering

STATUS: Incomplete / Not functional

Mock data was generated using Faker library instead.
See: generate_mock_data.py for the working data pipeline.

This file is kept only to show the scraping approach attempted.
"""

# ---- Code below is incomplete and will not run successfully ----

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
import time

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your_password_here",
    database="business_dashboard"
)
cursor = conn.cursor()
print("Mysql Connected")

# ── Setup Chrome ──────────────────────────────────────────────
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# ── Config ────────────────────────────────────────────────────
CITIES = ["Mumbai","Delhi","Banglore","Chennai","Pune"]
CATEGORIES = ["Restraunt","Hotels","Hospitals","Gyms"]
PAGES_PER_COMBO = 3
BASE_URL = "https://www.justdial.com/Mumbai/Restaurants"
TOTAL_PAGES = 5
all_data = []

# ── Scrape ────────────────────────────────────────────────────
for page in range(1, TOTAL_PAGES + 1):

    if page == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}/page-{page}"

    print(f"\nScraping page {page}: {url}")
    driver.get(url)
    time.sleep(3)  


    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 800)")
        time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    listings = soup.find_all("li", class_=lambda c: c and "cntanr" in c)

    print(f"Listings found: {len(listings)}")

    for city in CITIES:
        for category in CATEGORIES:
            print(f"\n{'='*50}")
            print(f"Scraping: {city} → {category}")
            print(f"{'='*50}")

            for page in range(1, PAGES_PER_COMBO + 1):
                if page == 1:
                    url = f"https://www.justdial.com/{city}/{category}"
                else:
                    url = f"https://www.justdial.com/{city}/{category}/page-{page}"

                print(f"  Page {page}: {url}")

                try:
                    driver.get(url)
                    time.sleep(3)

                # Scroll to load all listings
                    for _ in range(5):
                        driver.execute_script("window.scrollBy(0, 800)")
                        time.sleep(1)

                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    listings = soup.find_all("li", class_=lambda c: c and "cntanr" in c)

                    print(f"  Listings found: {len(listings)}")

                    for listing in listings:
                        try:
                            name    = listing.find("span", class_=lambda c: c and "lng_nu" in c)
                            phone   = listing.find("p",    class_=lambda c: c and "contact" in c)
                            address = listing.find("span", class_=lambda c: c and "cont_fl_addr" in c)
                            rating  = listing.find("span", class_=lambda c: c and "rt_count" in c)

                            data = {
                                "business_name": name.text.strip()    if name    else "N/A",
                                "category":      category,
                                "city":          city,
                                "address":       address.text.strip() if address else "N/A",
                                "phone":         phone.text.strip()   if phone   else "N/A",
                                "rating":        rating.text.strip()  if rating  else "N/A",
                                "source":        "Justdial",
                                "page":          page
                            }
                            all_data.append(data)

                        except Exception as e:
                            print(f"  Skipped a listing: {e}")
                            continue

                except Exception as e:
                        print(f"  Page failed: {e} — moving on")
                        continue

                print(f"  Total so far: {len(all_data)} listings")

                if len(all_data) >= 500:
                        print("\n✅ 500+ listings reached. Stopping early.")
                        break

                time.sleep(2)  # polite delay between pages

            if len(all_data) >= 500:
                    break

        if len(all_data) >= 500:
                break

driver.quit()
print("\nChrome Closed")
# ── Save ──────────────────────────────────────────────────────
print(f"\nTotal listings scraped: {len(all_data)}")

if all_data:
    df = pd.DataFrame(all_data)
    df.drop_duplicates(subset=["business_name", "city", "phone"], inplace=True)
    print(f"After removing duplicates: {len(df)} listings")

    query ='''Insert into listing_master(business_name,category,city,address,phone,source)
           VALUES (%(business_name)s , %(category)s, %(city)s, %(address)s, %(phone)s ,%(source)s)
           '''
    cursor.executemany(query,df.to_dict("recors"))
    conn.commit()
    print(f"Inserted {cursor.rowcount}record into MySQL")

    df.to_csv("business_listings.csv", index=False, encoding="utf-8")
    print("Saved: business_listings.csv")
else:
    print("No data found. Check class names.")

cursor.close()
conn.close()
print("Mysql Connection Closed")