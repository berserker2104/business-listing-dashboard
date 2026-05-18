# 🏢 Business Listings Dashboard

A full-stack data dashboard that collects, stores, and visualizes 
business listings data across Indian cities.

---

## 🛠️ Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Frontend  | React.js, Recharts|
| Backend   | FastAPI (Python)  |
| Database  | MySQL             |
| Scraping  | Faker (mock data) |

---

## 📁 Project Structure

```
business-listings-dashboard/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── scraper.py
│   ├── mock_data.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 8+

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/business-listings-dashboard.git
cd business-listings-dashboard
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

Create your `.env` file:
```bash
cp .env.example .env
Fill in your MySQL credentials
```

Run the FastAPI server:
```bash
uvicorn main:app --reload
```

API runs at: `http://localhost:8000`  
Swagger Docs: `http://localhost:8000/docs`

### 3. Seed the Database
```bash
python scraper.py
This generates and inserts 500+ mock business listings
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm start
```

Dashboard runs at: `http://localhost:3000`

---

## 🔌 API Endpoints

| Method | Endpoint              | Description              |
|--------|-----------------------|--------------------------|
| POST   | `/listings/bulk`      | Insert bulk listings     |
| GET    | `/dashboard/city`     | City-wise business count |
| GET    | `/dashboard/category` | Category-wise count      |
| GET    | `/dashboard/source`   | Source-wise count        |

---

## 📊 Dashboard Features

- **City-wise** business count — Bar Chart
- **Category-wise** business count — Pie Chart
- **Source-wise** business count — Bar Chart

---

## 🌐 Data Collection Approach

> **Attempted:** Live scraping from Justdial  
> **Issue:** Justdial actively blocks automated requests  
> (CAPTCHA, rate limiting, IP blocking)
>
> **Solution:** Used Python's `Faker` library to generate 
> realistic mock data with:
> - 20+ Indian cities
> - 10+ business categories  
> - Multiple source labels (Justdial, Sulekha, Google)
> - 500+ unique listings

This approach was chosen as per assignment guidelines which 
permit mock data when scraping is blocked.

---

## ⚠️ Challenges Faced

1. **Justdial scraping blocked** — Solved using Faker mock data
2. **CORS issues** between React and FastAPI — Fixed with 
   FastAPI CORS middleware
3. **MySQL connection pooling** — Handled with SQLAlchemy

---

## 📦 Environment Variables
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=business_listings

---

## 👤 Author

Shubham Khairnar   
[LinkedIn](— https://www.linkedin.com/in/shubham-khairnar-31502a231 )