import os
import math
import random
import time
import re
from typing import List, Dict, Any, Tuple

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_geolocation import streamlit_geolocation

# ========= Config / setup =========

load_dotenv()
API_KEY = st.secrets["GOOGLE_API_KEY"]

PLACES_NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PLACES_AUTOCOMPLETE_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Defaults
DEFAULT_MIN_RATING = 4.0
DEFAULT_MIN_REVIEWS = 20
DEFAULT_RADIUS_METERS = 1500
DEFAULT_NUM_CHOICES = 3

# Delivery-only keywords to exclude
DELIVERY_ONLY_KEYWORDS = [
    "delivery", "cloud kitchen", "ghost kitchen",
    "virtual kitchen", "dark kitchen", "online only",
]

# Chain blacklist
FAST_FOOD_KEYWORDS = [
    "mcdonald", "kfc", "burger king", "subway",
    "pizza hut", "domino", "starbucks", "coffee bean",
    "texas chicken", "jollibee", "carl's jr",
    "long john", "shake shack", "five guys",
    "ya kun", "yakun", "toast box", "old chang kee",
    "old changkee", "liho", "koi", "paris baguette",
    "breadtalk", "stuff'd", "stuffd", "sushi express",
    "saizeriya", "dian xiao er", "swensen", "swensen's",
    "killiney", "fun toast",
]

HAWKER_CENTRE_KEYWORDS = [
    "hawker centre", "hawker center",
    "food centre", "food center",
    "food court", "market & food centre",
    "kopitiam", "coffee shop",
]

st.set_page_config(
    page_title="NomNom",
    layout="centered",
)

# === Website Design ===
# Replace your BASE_CSS variable (around line 61) with this:

BASE_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* === GLOBAL === */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    }
    
    body, .stApp, .main {
        background-color: #121212 !important;
    }
    
    /* === CONTAINER === */
    .block-container {
        max-width: 560px !important;
        margin: 0 auto !important;
        padding: 3rem 1.5rem 4rem 1.5rem !important;
    }
    
    /* === HEADER === */
    h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #ffe066 !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.04em !important;
        line-height: 1 !important;
    }
    
    h4 {
        font-size: 1.125rem !important;
        font-weight: 400 !important;
        color: #66c2c2 !important;
        text-align: center !important;
        margin-top: 0 !important;
        margin-bottom: 3rem !important;
    }
    
    /* === SECTION HEADERS === */
    .section-header {
        font-size: 1rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #ffe066 !important;
        text-align: center !important;
        margin: 3rem auto 1.5rem auto !important;
        padding: 0.75rem 1.5rem !important;
        background: linear-gradient(135deg, rgba(255, 224, 102, 0.08) 0%, rgba(255, 224, 102, 0.02) 100%) !important;
        border-radius: 0.75rem !important;
        border: 1px solid rgba(255, 224, 102, 0.2) !important;
        display: block !important;
        width: fit-content !important;
    }
    
    .section-spacer {
        height: 0 !important;
    }
    
    /* === LABELS === */
    label, 
    div[data-testid="stRadio"] > label,
    div[data-testid="stTextInput"] > label,
    div[data-testid="stSelectbox"] > label,
    div[data-testid="stSlider"] > label {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #a3a3a3 !important;
        text-align: center !important;
        justify-content: center !important;
        display: flex !important;
    }
    
    /* === RADIO BUTTONS === */
    div[data-testid="stRadio"] {
        text-align: center !important;
    }
    
    div[data-testid="stRadio"] > div {
        justify-content: center !important;
        gap: 0.75rem !important;
        flex-wrap: wrap !important;
    }
    
    div[data-testid="stRadio"] label[data-baseweb="radio"] {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 0.75rem !important;
        padding: 0.875rem 1.5rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
        border-color: #404040 !important;
        background-color: #1f1f1f !important;
    }
    
    div[data-testid="stRadio"] input:checked + div {
        background-color: #ffe066 !important;
        color: #121212 !important;
    }
    
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background-color: #1a1a1a !important;
        border-color: #ffe066 !important;
        box-shadow: 0 0 0 3px rgba(255, 224, 102, 0.1) !important;
    }
    
    /* === TEXT INPUTS === */
    div[data-testid="stTextInput"] {
        text-align: center !important;
    }
    
    input[type="text"] {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 0.75rem !important;
        color: #fafafa !important;
        padding: 0.875rem 1.25rem !important;
        font-size: 0.9375rem !important;
        text-align: center !important;
        transition: all 0.2s ease !important;
    }
    
    input[type="text"]:focus {
        border-color: #ffe066 !important;
        box-shadow: 0 0 0 3px rgba(255, 224, 102, 0.1) !important;
        outline: none !important;
        background-color: #1f1f1f !important;
    }
    
    input[type="text"]::placeholder {
        color: #525252 !important;
        text-align: center !important;
    }
    
    /* === SELECT BOXES === */
    div[data-testid="stSelectbox"] {
        text-align: center !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 0.75rem !important;
        min-height: 3rem !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #404040 !important;
    }
    
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] > div > div {
        color: #fafafa !important;
    }
    
    /* === SLIDERS === */
    [data-testid="stSlider"] {
        padding: 1.5rem 0 1rem 0 !important;
    }
    
    [data-testid="stSlider"] .rc-slider-rail {
        background-color: #1a1a1a !important;
        height: 4px !important;
        border-radius: 2px !important;
    }
    
    [data-testid="stSlider"] .rc-slider-track {
        background: linear-gradient(90deg, #ffe066 0%, #ffd93d 100%) !important;
        height: 4px !important;
        border-radius: 2px !important;
    }
    
    [data-testid="stSlider"] .rc-slider-handle {
        border: 3px solid #ffe066 !important;
        background-color: #121212 !important;
        width: 18px !important;
        height: 18px !important;
        margin-top: -7px !important;
        box-shadow: 0 2px 12px rgba(255, 224, 102, 0.4) !important;
        opacity: 1 !important;
    }
    
    [data-testid="stSlider"] .rc-slider-handle:hover,
    [data-testid="stSlider"] .rc-slider-handle:active {
        border-color: #ffd93d !important;
        box-shadow: 0 4px 20px rgba(255, 224, 102, 0.6) !important;
    }
    
    /* === BUTTONS === */
    div[data-testid="stButton"] {
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
    }
    
    div[data-testid="stButton"] > button {
        background-color: #1a1a1a !important;
        color: #fafafa !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 0.75rem !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        transition: all 0.2s ease !important;
        min-width: 200px !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #1f1f1f !important;
        border-color: #404040 !important;
        transform: translateY(-1px) !important;
    }
    
    /* === PRIMARY BUTTON (Find Restaurants) === */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ffe066 0%, #ffd93d 100%) !important;
        color: #121212 !important;
        border: none !important;
        border-radius: 1rem !important;
        padding: 1.125rem 3rem !important;
        font-weight: 800 !important;
        font-size: 1.0625rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-top: 2.5rem !important;
        min-width: 100% !important;
        box-shadow: 0 8px 32px rgba(255, 224, 102, 0.35), 0 0 64px rgba(255, 224, 102, 0.15) !important;
    }
    
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ffd93d 0%, #ffeb70 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 40px rgba(255, 224, 102, 0.5), 0 0 80px rgba(255, 224, 102, 0.25) !important;
    }
    
    button[kind="primary"]:active {
        transform: translateY(0) !important;
    }
    
    @keyframes subtleGlow {
        0%, 100% {
            box-shadow: 0 8px 32px rgba(255, 224, 102, 0.35), 0 0 64px rgba(255, 224, 102, 0.15);
        }
        50% {
            box-shadow: 0 8px 36px rgba(255, 224, 102, 0.4), 0 0 72px rgba(255, 224, 102, 0.2);
        }
    }
    
    button[kind="primary"] {
        animation: subtleGlow 3s ease-in-out infinite !important;
    }
    
    /* === RESULT CARDS === */
    .results-container {
        margin-top: 2rem !important;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #1f1f1f 100%) !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 1rem !important;
        padding: 1.5rem 1.75rem !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
    }
    
    .result-card:hover {
        border-color: #ffe066 !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 40px rgba(255, 224, 102, 0.15) !important;
        background: linear-gradient(135deg, #1f1f1f 0%, #262626 100%) !important;
    }
    
    .result-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #fafafa !important;
        margin-bottom: 0.625rem !important;
        letter-spacing: -0.02em !important;
    }
    
    .result-meta {
        font-size: 0.875rem !important;
        color: #737373 !important;
        margin-bottom: 0.75rem !important;
        line-height: 1.5 !important;
    }
    
    .result-badge {
        display: inline-block !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #ffe066 !important;
        background-color: rgba(255, 224, 102, 0.1) !important;
        border: 1px solid rgba(255, 224, 102, 0.2) !important;
        border-radius: 0.5rem !important;
        padding: 0.375rem 0.875rem !important;
        margin-right: 0.5rem !important;
        margin-top: 0.25rem !important;
    }
    
    .result-card a {
        color: #ffe066 !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        display: inline-block !important;
        margin-top: 0.75rem !important;
        border-bottom: 1.5px solid rgba(255, 224, 102, 0.3) !important;
        padding-bottom: 2px !important;
    }
    
    .result-card a:hover {
        color: #ffd93d !important;
        border-bottom-color: #ffd93d !important;
    }
    
    /* === MESSAGES === */
    .stSuccess {
        background-color: rgba(255, 224, 102, 0.08) !important;
        border: 1px solid rgba(255, 224, 102, 0.2) !important;
        border-left: 3px solid #ffe066 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #fafafa !important;
        text-align: center !important;
    }
    
    .stInfo {
        background-color: rgba(115, 115, 115, 0.08) !important;
        border: 1px solid rgba(115, 115, 115, 0.2) !important;
        border-left: 3px solid #737373 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #a3a3a3 !important;
        text-align: center !important;
    }
    
    .stWarning {
        background-color: rgba(251, 146, 60, 0.08) !important;
        border: 1px solid rgba(251, 146, 60, 0.2) !important;
        border-left: 3px solid #fb923c !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #fafafa !important;
        text-align: center !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.08) !important;
        border: 1px solid rgba(239, 68, 68, 0.2) !important;
        border-left: 3px solid #ef4444 !important;
        border-radius: 0.75rem !important;
        padding: 1rem !important;
        color: #fafafa !important;
        text-align: center !important;
    }
    
    /* === ANIMATIONS === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card {
        animation: fadeInUp 0.5s ease-out backwards;
    }
    
    .result-card:nth-child(1) { animation-delay: 0.1s; }
    .result-card:nth-child(2) { animation-delay: 0.2s; }
    .result-card:nth-child(3) { animation-delay: 0.3s; }
    .result-card:nth-child(4) { animation-delay: 0.4s; }
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)

if not API_KEY:
    st.error("GOOGLE_API_KEY not found. Set it in .env as GOOGLE_API_KEY=...")
    st.stop()

# Session state
if "seen_place_ids" not in st.session_state:
    st.session_state["seen_place_ids"] = []
if "place_candidates" not in st.session_state:
    st.session_state["place_candidates"] = []
if "place_candidate_index" not in st.session_state:
    st.session_state["place_candidate_index"] = 0
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False
if "results_data" not in st.session_state:
    st.session_state["results_data"] = None

# ========= Geocoding helpers =========

def get_place_latlng(place_id: str) -> Tuple[float, float]:
    """Use Place Details API to get lat/lng from place_id."""
    params = {
        "key": API_KEY,
        "place_id": place_id,
        "fields": "geometry",
    }
    resp = requests.get(PLACES_DETAILS_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status")
    if status not in ("OK", "ZERO_RESULTS"):
        raise RuntimeError(f"Place Details error: {status} - {data.get('error_message')}")

    result = data.get("result", {})
    loc = result.get("geometry", {}).get("location")
    if not loc:
        raise RuntimeError("No geometry for that place_id.")

    return float(loc["lat"]), float(loc["lng"])


def autocomplete_places(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Places Autocomplete: get candidate locations."""
    params = {
        "key": API_KEY,
        "input": query,
        "region": "sg",
    }
    resp = requests.get(PLACES_AUTOCOMPLETE_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    status = data.get("status")
    if status not in ("OK", "ZERO_RESULTS"):
        raise RuntimeError(f"Autocomplete error: {status} - {data.get('error_message')}")

    preds = data.get("predictions", [])
    if not preds:
        return []

    results: List[Dict[str, Any]] = []
    for p in preds[:max_results]:
        place_id = p.get("place_id")
        desc = p.get("description")
        if not place_id or not desc:
            continue
        try:
            lat, lng = get_place_latlng(place_id)
        except Exception:
            continue
        results.append(
            {
                "description": desc,
                "place_id": place_id,
                "lat": lat,
                "lng": lng,
            }
        )

    return results

# ========= Nearby search logic =========

def get_nearby_places(
    lat: float,
    lng: float,
    radius: int,
    search_type: str = "All (Food & Drinks)",
    cuisine_filter: str = "All Cuisines",
) -> List[Dict[str, Any]]:
    """Use Places Nearby Search to get eateries based on type and cuisine filter."""
    
    # Map user selection to Google Places API types - MORE AGGRESSIVE
    if search_type == "Food only":
        place_types = ["restaurant"]  # Only restaurants, no delivery/takeaway
    elif search_type == "Drinks only":
        place_types = ["cafe", "bar"]
    else:  # "All (Food & Drinks)"
        place_types = ["restaurant", "cafe"]  # Exclude meal_delivery and meal_takeaway

    combined: Dict[str, Dict[str, Any]] = {}

    for ptype in place_types:
        params = {
            "key": API_KEY,
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": ptype,
        }
        
        # Add cuisine-specific keyword if not "All Cuisines"
        if cuisine_filter != "All Cuisines":
            params["keyword"] = cuisine_filter.lower()

        while True:
            resp = requests.get(PLACES_NEARBY_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            status = data.get("status")
            if status not in ("OK", "ZERO_RESULTS"):
                raise RuntimeError(f"Nearby Search error: {status} - {data.get('error_message')}")

            for r in data.get("results", []):
                pid = r.get("place_id")
                key = pid or (f"{(r.get('name') or '').lower()}|{(r.get('vicinity') or '').lower()}")
                if key not in combined:
                    combined[key] = r

            next_token = data.get("next_page_token")
            if not next_token:
                break
            time.sleep(2)
            params = {"key": API_KEY, "pagetoken": next_token}

    return list(combined.values())

# ========= Filtering / scoring =========

def filter_and_score_places(
    places: List[Dict[str, Any]],
    min_rating: float,
    min_reviews: int,
    price_filter: str,
    center_lat: float,
    center_lng: float,
) -> List[Dict[str, Any]]:
    """Apply filters and score places."""

    def haversine_m(lat1, lon1, lat2, lon2) -> float:
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    filtered: List[Dict[str, Any]] = []

    for p in places:
        name_raw = p.get("name") or ""
        name = name_raw.lower()
        rating = p.get("rating")
        reviews = p.get("user_ratings_total", 0)
        price = p.get("price_level")
        loc = p.get("geometry", {}).get("location", {})
        plat, plng = loc.get("lat"), loc.get("lng")
        types = p.get("types", [])

        # Exclude chains
        if any(k in name for k in FAST_FOOD_KEYWORDS):
            continue
        
        # Exclude obvious centres / markets
        if any(k in name for k in HAWKER_CENTRE_KEYWORDS):
            continue
        
        # Exclude delivery-only places
        if any(k in name for k in DELIVERY_ONLY_KEYWORDS):
            continue
        
        # More aggressive: exclude if it's ONLY meal_delivery or meal_takeaway
        if "meal_delivery" in types and "restaurant" not in types and "cafe" not in types:
            continue
        if "meal_takeaway" in types and "restaurant" not in types and "cafe" not in types:
            continue
            
        if rating is None or plat is None or plng is None:
            continue
        if rating < min_rating or reviews < min_reviews:
            continue

        if price_filter == "Cheap only (Google 0–1)":
            if price is None or price > 1:
                continue
        elif price_filter == "Exclude expensive (Google >2)":
            if price is not None and price > 2:
                continue

        dist_m = haversine_m(center_lat, center_lng, plat, plng)

        cheap_bonus = 0.0
        if price in (0, 1):
            cheap_bonus = 0.4

        score = (
            2.0 * rating
            + 0.6 * math.log1p(reviews)
            - 0.001 * dist_m
            + cheap_bonus
        )
        p["_score"] = score
        p["_distance_m"] = dist_m

        filtered.append(p)

    def _normalize_name(n: str) -> str:
        n = (n or "").lower()
        n = re.sub(r"\(.*?\)", "", n)
        n = re.sub(r"[^a-z0-9\s]", " ", n)
        n = re.sub(r"\s+", " ", n).strip()
        return n

    seen = set()
    deduped: List[Dict[str, Any]] = []
    for p in sorted(filtered, key=lambda x: x["_score"], reverse=True):
        norm = _normalize_name(p.get("name", ""))
        if not norm:
            pid = p.get("place_id")
            if pid and pid not in seen:
                seen.add(pid)
                deduped.append(p)
            continue

        if norm in seen:
            continue
        seen.add(norm)
        deduped.append(p)

    return deduped

def build_gmaps_url(place_id: str) -> str:
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"

def pick_new_random_places(filtered: List[Dict[str, Any]], k: int) -> List[Dict[str, Any]]:
    """Randomly pick k places not shown yet this session."""
    seen_ids = set(st.session_state["seen_place_ids"])
    remaining = [p for p in filtered if p.get("place_id") not in seen_ids]

    if not remaining and filtered:
        st.session_state["seen_place_ids"] = []
        seen_ids = set()
        remaining = filtered

    if not remaining:
        return []

    k = min(k, len(remaining))
    picks = random.sample(remaining, k)

    for p in picks:
        pid = p.get("place_id")
        if pid and pid not in seen_ids:
            st.session_state["seen_place_ids"].append(pid)

    return picks

# ========= UI =========

# Header
st.markdown(
    """
    <div style="text-align: center;">
        <h1>NomNom</h1>
        <h3>Dinner, simplified.</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# === LOCATION ===
st.markdown('<div class="section-header">Location</div>', unsafe_allow_html=True)

location_mode = st.radio(
    "",
    [
        "Use current location (GPS)",
        "Search by area",
    ],
    index=0,
    label_visibility="collapsed"
)

effective_lat = None
effective_lng = None

if location_mode == "Use current location (GPS)":
    loc = streamlit_geolocation()
    if isinstance(loc, dict) and loc.get("latitude") is not None:
        effective_lat = float(loc["latitude"])
        effective_lng = float(loc["longitude"])
        st.success(f"Location detected: {effective_lat:.5f}, {effective_lng:.5f}")
    else:
        st.info("Waiting for location permission...")
else:
    query = st.text_input(
        "Search for an area or landmark",
        placeholder="e.g. Trastevere, Piazza Navona",
    )

    if st.button("Search", key="search_places", use_container_width=True):
        q = query.strip()
        if not q:
            st.error("Please enter a location to search.")
        else:
            try:
                candidates = autocomplete_places(q, max_results=5)
                st.session_state["place_candidates"] = candidates
                st.session_state["place_candidate_index"] = 0
            except Exception as e:
                st.error(f"Search failed: {e}")
                st.session_state["place_candidates"] = []

    candidates = st.session_state.get("place_candidates", [])
    if candidates:
        idx = st.selectbox(
            "Select location",
            options=list(range(len(candidates))),
            format_func=lambda i: candidates[i]["description"],
            key="candidate_select",
        )
        st.session_state["place_candidate_index"] = idx
        chosen = candidates[idx]
        effective_lat, effective_lng = chosen["lat"], chosen["lng"]

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# === FILTERS ===
st.markdown('<div class="section-header">Preferences</div>', unsafe_allow_html=True)

# Food/Drink type filter
search_type = st.selectbox(
    "Type",
    [
        "All (Food & Drinks)",
        "Food only",
        "Drinks only",
    ],
    index=0,
)

# Cuisine filter
cuisine_filter = st.selectbox(
    "Cuisine",
    [
        "All Cuisines",
        "Italian",
        "Chinese",
        "Japanese",
        "Korean",
        "Thai",
        "Vietnamese",
        "Indian",
        "French",
        "Mediterranean",
        "Greek",
        "Mexican",
        "American",
        "Steakhouse",
        "Seafood",
        "Local / Asian",
        "Fusion",
    ],
    index=0,
)

min_rating = st.slider(
    "Minimum rating",
    min_value=4.0,
    max_value=5.0,
    value=DEFAULT_MIN_RATING,
    step=0.1,
)

min_reviews = st.slider(
    "Minimum reviews",
    min_value=0,
    max_value=500,
    value=DEFAULT_MIN_REVIEWS,
    step=20,
)

price_filter = st.selectbox(
    "Price range",
    [
        "Any price",
        "Cheap only (Google 0–1)",
        "Exclude expensive (Google >2)",
    ],
    index=0,
)

radius = st.slider(
    "Search radius (meters)",
    min_value=200,
    max_value=5000,
    value=DEFAULT_RADIUS_METERS,
    step=100,
)

num_choices = st.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=DEFAULT_NUM_CHOICES,
)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

# === GO BUTTON ===
go = st.button("Find Restaurants", key="go_button", type="primary", use_container_width=True)

# === RESULTS LOGIC ===
if go:
    if effective_lat is None or effective_lng is None:
        st.error("Please set your location first.")
        st.session_state["show_results"] = False
    else:
        with st.spinner("Searching for restaurants..."):
            try:
                raw_places = get_nearby_places(
                    effective_lat, 
                    effective_lng, 
                    radius=radius, 
                    search_type=search_type,
                    cuisine_filter=cuisine_filter
                )
            except Exception as e:
                st.error(f"Search error: {e}")
                st.session_state["show_results"] = False
                st.stop()

            if not raw_places:
                st.warning("No places found. Try increasing your search radius.")
                st.session_state["show_results"] = False
            else:
                ranked = filter_and_score_places(
                    raw_places,
                    min_rating=min_rating,
                    min_reviews=min_reviews,
                    price_filter=price_filter,
                    center_lat=effective_lat,
                    center_lng=effective_lng,
                )

                if not ranked:
                    st.warning("No results match your criteria. Try adjusting your filters.")
                    st.session_state["show_results"] = False
                else:
                    picks = pick_new_random_places(ranked, k=num_choices)
                    if not picks:
                        st.warning("No new places to show. Try adjusting your filters or search again.")
                        st.session_state["show_results"] = False
                    else:
                        st.session_state["show_results"] = True
                        st.session_state["results_data"] = picks

# === DISPLAY RESULTS ===
if st.session_state.get("show_results", False) and st.session_state.get("results_data"):
    st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
    
    picks = st.session_state["results_data"]
    st.success(f"Found {len(picks)} restaurant(s)")
    
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
    for p in picks:
        name = p.get("name", "Unknown")
        rating = p.get("rating", "?")
        reviews = p.get("user_ratings_total", 0)
        price = p.get("price_level", None)
        addr = p.get("vicinity", "")
        place_id = p.get("place_id", "")
        dist_m = p.get("_distance_m", None)

        maps_url = build_gmaps_url(place_id) if place_id else None

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="result-title">{name}</div>', unsafe_allow_html=True)

        meta_line = []
        meta_line.append(f"★ {rating:.1f}" if isinstance(rating, (int, float)) else f"★ {rating}")
        meta_line.append(f"{reviews} reviews")
        if dist_m is not None:
            if dist_m < 1000:
                meta_line.append(f"{int(dist_m)}m away")
            else:
                meta_line.append(f"{dist_m/1000:.1f}km away")

        st.markdown(
            '<div class="result-meta">' + " · ".join(meta_line) + "</div>",
            unsafe_allow_html=True,
        )

        badge_line = []
        if price is None:
            badge_line.append("Price unknown")
        else:
            price_symbols = ["$", "$", "$$", "$$", "$$$"]
            badge_line.append(f"{price_symbols[min(price, 4)]}")

        if badge_line:
            st.markdown(
                "".join(f'<span class="result-badge">{b}</span>' for b in badge_line),
                unsafe_allow_html=True,
            )

        if addr:
            st.markdown(
                f'<div class="result-meta" style="margin-top: 8px;">{addr}</div>',
                unsafe_allow_html=True,
            )

        if maps_url:
            st.markdown(f"[View on Google Maps]({maps_url})")

        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
