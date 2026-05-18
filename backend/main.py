from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import listings, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business Listings API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings.router,prefix="/api")
app.include_router(dashboard.router,prefix="/api")

@app.get("/")
def root():
    return {"message": "Business Listings API is running!"}