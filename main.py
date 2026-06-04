import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any

app = FastAPI(
    title="Awsar Setu API",
    description="Production-grade social infrastructure platform for scheme routing.",
    version="2.0.0"
)

# Mega-Database Matrix
SCHEMES_DATABASE: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)",
        "level": "NATIONAL",
        "state_code": None,
        "min_age": 18,
        "max_age": 40,
        "benefit": "Minimum assured pension of Rs 3,000 per month after reaching the age of 60.",
        "eligibility": "Unorganized worker, monthly income Rs 15,000 or less, non-income tax payee.",
        "process": "Visit nearest Common Services Centre (CSC) with Aadhaar and Savings Bank passbook."
    },
    {
        "id": 2,
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "level": "NATIONAL",
        "state_code": None,
        "min_age": 0,
        "max_age": 10,
        "benefit": "High-interest savings account (8.2%) with tax exemptions, maturing at age 21.",
        "eligibility": "Opened by parent/guardian for a girl child resident in India; max 2 per household.",
        "process": "Visit authorized Post Office or commercial bank branch with birth certificate."
    },
    {
        "id": 3,
        "name": "PM-KISAN",
        "level": "NATIONAL",
        "state_code": None,
        "min_age": 18,
        "max_age": 100,
        "benefit": "Rs 6,000 per year distributed in three equal installments of Rs 2,000 via DBT.",
        "eligibility": "Landholding farmer families owning cultivable land. Institutional holders excluded.",
        "process": "Self-registration via PM-KISAN online portal using Aadhaar-linked OTP."
    },
    {
        "id": 4,
        "name": "Subhadra Yojana",
        "level": "STATE",
        "state_code": "OR",
        "min_age": 21,
        "max_age": 60,
        "benefit": "Rs 10,000 annually for 5 years (Total Rs 50,000) paid on Rakhi Purnima and Women's Day.",
        "eligibility": "Permanent female resident of Odisha, family holds NFSA/SFSS card or income under Rs 2.5 Lakh.",
        "process": "Submit physical form at Mo Seva Kendras or Anganwadi Centres with Aadhaar e-KYC."
    },
    {
        "id": 5,
        "name": "KALIA Scheme",
        "level": "STATE",
        "state_code": "OR",
        "min_age": 18,
        "max_age": 100,
        "benefit": "Rs 10,000 per year provided for livelihood support.",
        "eligibility": "Permanent resident of Odisha, small/marginal farmer or landless agricultural laborer.",
        "process": "Apply online via unified KALIA portal or through Gram Panchayat nodal officer."
    },
    {
        "id": 6,
        "name": "Biju Swasthya Kalyan Yojana (BSKY)",
        "level": "STATE",
        "state_code": "OR",
        "min_age": 0,
        "max_age": 120,
        "benefit": "Cashless health coverage up to Rs 5 Lakh/year for family (Rs 10 Lakh for female members).",
        "eligibility": "All families holding a National Food Security Act (NFSA) or SFSS card in Odisha.",
        "process": "Present the NFSA/SFSS card directly at any empanelled private or government hospital."
    }
]

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the premium index.html visual interface at the root URL path."""
    filepath = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Awsar Setu UI file loading... Refresh repository or deploy updates.</h1>"

@app.get("/api/v2/schemes")
def get_personalized_schemes(
    age: int = Query(..., description="Age of the applicant"),
    state: str = Query(..., description="Two letter state code, e.g., OR for Odisha")
):
    state_upper = state.upper()
    
    national_schemes = [
        scheme for scheme in SCHEMES_DATABASE
        if scheme["level"] == "NATIONAL" and scheme["min_age"] <= age <= scheme["max_age"]
    ]
    
    state_schemes = [
        scheme for scheme in SCHEMES_DATABASE
        if scheme["level"] == "STATE" and scheme["state_code"] == state_upper and scheme["min_age"] <= age <= scheme["max_age"]
    ]
    
    return {
        "user_meta": {
            "requested_age": age,
            "requested_state": state_upper
        },
        "national_section": {
            "count": len(national_schemes),
            "schemes": national_schemes
        },
        "state_section": {
            "count": len(state_schemes),
            "schemes": state_schemes
        }
    }
