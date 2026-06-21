import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Awsar Setu API",
    description="Production-grade social infrastructure platform for scheme routing.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Core database for the API. The browser UI also has a larger embedded catalog so
# the app stays useful even if a hosting platform blocks a network request.
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
        "process": "Visit nearest Common Services Centre (CSC) with Aadhaar and Savings Bank passbook.",
    },
    {
        "id": 2,
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "level": "NATIONAL",
        "state_code": None,
        "min_age": 0,
        "max_age": 10,
        "benefit": "High-interest savings account with tax exemptions, maturing at age 21.",
        "eligibility": "Opened by parent or guardian for a girl child resident in India; max 2 per household.",
        "process": "Visit authorized Post Office or commercial bank branch with birth certificate.",
    },
    {
        "id": 3,
        "name": "PM-KISAN",
        "level": "NATIONAL",
        "state_code": None,
        "min_age": 18,
        "max_age": 100,
        "benefit": "Rs 6,000 per year distributed in three equal installments via DBT.",
        "eligibility": "Landholding farmer families owning cultivable land. Institutional holders excluded.",
        "process": "Self-registration via PM-KISAN online portal using Aadhaar-linked OTP.",
    },
    {
        "id": 4,
        "name": "Subhadra Yojana",
        "level": "STATE",
        "state_code": "OR",
        "min_age": 21,
        "max_age": 60,
        "benefit": "Rs 10,000 annually for 5 years paid in two installments.",
        "eligibility": "Permanent female resident of Odisha with NFSA/SFSS card or qualifying income.",
        "process": "Submit physical form at Mo Seva Kendras or Anganwadi Centres with Aadhaar e-KYC.",
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
        "process": "Apply online via unified KALIA portal or through Gram Panchayat nodal officer.",
    },
    {
        "id": 6,
        "name": "Biju Swasthya Kalyan Yojana (BSKY)",
        "level": "STATE",
        "state_code": "OR",
        "min_age": 0,
        "max_age": 120,
        "benefit": "Cashless health coverage for eligible Odisha families.",
        "eligibility": "Families holding a National Food Security Act (NFSA) or SFSS card in Odisha.",
        "process": "Present the NFSA/SFSS card directly at any empanelled private or government hospital.",
    },
]

STATE_ALIASES = {
    "ODISHA": "OR",
    "OR": "OR",
    "UP": "UP",
    "UTTAR PRADESH": "UP",
    "MAHARASHTRA": "MH",
    "MH": "MH",
    "BIHAR": "BR",
    "BR": "BR",
    "TAMIL NADU": "TN",
    "TN": "TN",
}

OLD_API_BASE = "https://awsar-setu-v2.vercel.app"


def normalize_state(state: str) -> str:
    normalized = state.strip().upper()
    return STATE_ALIASES.get(normalized, normalized[:2])


def scheme_matches(scheme: Dict[str, Any], age: int, state_code: Optional[str] = None) -> bool:
    if not (scheme["min_age"] <= age <= scheme["max_age"]):
        return False
    if scheme["level"] == "STATE":
        return scheme.get("state_code") == state_code
    return True


@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serve the web interface at the root URL path."""
    filepath = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        return html.replace(OLD_API_BASE, "")
    return "<h1>Awsar Setu is running.</h1><p>index.html was not found in this deployment.</p>"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "awsar-setu-v2"}


@app.get("/api/v2/schemes")
def get_personalized_schemes(
    age: int = Query(..., ge=0, le=120, description="Age of the applicant"),
    state: str = Query(..., min_length=2, description="State name or code, e.g. Odisha or OR"),
):
    state_code = normalize_state(state)

    national_schemes = [
        scheme
        for scheme in SCHEMES_DATABASE
        if scheme["level"] == "NATIONAL" and scheme_matches(scheme, age)
    ]

    state_schemes = [
        scheme
        for scheme in SCHEMES_DATABASE
        if scheme["level"] == "STATE" and scheme_matches(scheme, age, state_code)
    ]

    return {
        "user_meta": {
            "requested_age": age,
            "requested_state": state,
            "state_code": state_code,
        },
        "national": national_schemes,
        "state": state_schemes,
        "national_section": {
            "count": len(national_schemes),
            "schemes": national_schemes,
        },
        "state_section": {
            "count": len(state_schemes),
            "schemes": state_schemes,
        },
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
