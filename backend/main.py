import sys
import os
from datetime import datetime

# Add current directory to path so Python can find modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, Ad
from schemas import AdCreate, AdResponse
from telegram_bot import send_to_telegram

# Create FastAPI app
app = FastAPI(title="Classifieds API", description="Telegram Classifieds Bot API", version="1.0.0")

# Enable CORS (so frontend can talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== API ENDPOINTS ====================

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Classifieds API", "docs": "/docs"}


# CREATE an ad
@app.post("/ads", response_model=AdResponse)
def create_ad(ad: AdCreate, db: Session = Depends(get_db)):
    # Create new ad in database
    db_ad = Ad(
        title=ad.title,
        price=ad.price,
        description=ad.description,
        category=ad.category,
        contact=ad.contact,
        created_at=datetime.now()
    )
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)

    # Send to Telegram (ignore errors if VPN is off)
    try:
        send_to_telegram(ad)
    except Exception as e:
        print(f"Telegram error (ignored): {e}")

    return db_ad


# GET all ads
@app.get("/ads", response_model=list[AdResponse])
def get_ads(db: Session = Depends(get_db)):
    ads = db.query(Ad).order_by(Ad.created_at.desc()).all()
    return ads


# GET single ad by ID
@app.get("/ads/{ad_id}", response_model=AdResponse)
def get_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad


# UPDATE an ad
@app.put("/ads/{ad_id}", response_model=AdResponse)
def update_ad(ad_id: int, ad: AdCreate, db: Session = Depends(get_db)):
    db_ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not db_ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    db_ad.title = ad.title
    db_ad.price = ad.price
    db_ad.description = ad.description
    db_ad.category = ad.category
    db_ad.contact = ad.contact

    db.commit()
    db.refresh(db_ad)
    return db_ad


# DELETE an ad
@app.delete("/ads/{ad_id}")
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    db.delete(ad)
    db.commit()
    return {"message": "Ad deleted successfully"}