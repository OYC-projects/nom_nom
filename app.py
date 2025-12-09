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

# ========= GLOBAL CHAINS BLACKLIST (AGGRESSIVE) =========

# FAST FOOD - Global
GLOBAL_FAST_FOOD = [
    "mcdonald", "kfc", "burger king", "subway", "wendy's", "wendy",
    "pizza hut", "domino", "papa john", "little caesar",
    "taco bell", "chipotle", "qdoba", "moe's southwest",
    "popeyes", "church's chicken", "chick-fil-a", "chick fil a",
    "five guys", "shake shack", "in-n-out", "whataburger",
    "white castle", "sonic", "arby's", "arby", "carl's jr",
    "hardee's", "hardee", "jack in the box", "del taco",
    "long john silver", "a&w", "dairy queen", "baskin robbins",
    "dunkin", "krispy kreme", "tim horton", "panda express",
]

# COFFEE CHAINS - Global
GLOBAL_COFFEE = [
    "starbucks", "costa coffee", "costa", "coffee bean",
    "peet's coffee", "peet", "caribou coffee", "caribou",
    "dunkin", "tim hortons", "tim horton", "second cup",
    "gloria jean", "the coffee club", "cafe nero", "nero",
    "pret a manger", "pret", "eat.", "paul bakery",
]

# CASUAL DINING - Global
GLOBAL_CASUAL_DINING = [
    "applebee's", "applebee", "chili's", "chili", "tgi friday",
    "olive garden", "red lobster", "outback steakhouse", "outback",
    "buffalo wild wings", "hooters", "denny's", "denny",
    "ihop", "cheesecake factory", "california pizza kitchen", "cpk",
    "p.f. chang", "pf chang", "benihana", "hard rock cafe",
    "planet hollywood", "rainforest cafe", "cracker barrel",
]

# ASIAN CHAINS - Global/Regional
GLOBAL_ASIAN_CHAINS = [
    "yoshinoya", "sukiya", "matsuya", "tenya", "coco ichibanya",
    "ichiran", "ippudo", "ajisen", "marugame udon", "marugame",
    "genki sushi", "sushiro", "kura sushi", "hamazushi",
    "pepper lunch", "mos burger", "freshness burger",
    "din tai fung", "tim ho wan", "crystal jade", "paradise dynasty",
    "haidilao", "xiabu xiabu", "hai di lao",
]

# EUROPEAN CHAINS
EUROPEAN_CHAINS = [
    "greggs", "pret a manger", "eat.", "leon", "wasabi",
    "itsu", "yo! sushi", "wagamama", "nando's", "nando",
    "pizza express", "ask italian", "prezzo", "zizzi",
    "bella italia", "cafe rouge", "strada", "frankie & benny",
    "gourmet burger kitchen", "gbk", "byron burger", "five guys",
    "patisserie valerie", "paul", "le pain quotidien",
    "vapiano", "nordsee", "wienerwald", "block house",
    "l'osteria", "hans im glück", "hans im gluck",
    "flunch", "hippopotamus", "courtepaille", "buffalo grill",
    "quick", "brioche dorée", "brioche doree", "paul",
    "autogrill", "spontini", "rossopomodoro", "cioccolatitaliani",
    "old wild west", "america graffiti", "roadhouse",
]

# MIDDLE EASTERN CHAINS
MIDDLE_EAST_CHAINS = [
    "al baik", "albaik", "shawarma plus", "operation falafel",
    "just falafel", "zaroob", "firas sweets", "arz lebanese",
]

# CONVENIENCE STORES & SUPERMARKETS
CONVENIENCE_CHAINS = [
    "7-eleven", "7 eleven", "familymart", "family mart",
    "lawson", "circle k", "am/pm", "ampm", "wawa",
    "sheetz", "speedway", "cumberland farms", "kwik trip",
]

# BAKERY & DESSERT CHAINS - Global
GLOBAL_DESSERT_CHAINS = [
    "cinnabon", "auntie anne", "wetzel's pretzel", "wetzel",
    "godiva", "lindt", "sees candies", "garrett popcorn",
    "cold stone", "marble slab", "magnum", "haagen-dazs", "haagen dazs",
    "ben & jerry", "ben and jerry", "tcby", "pinkberry",
    "red mango", "tutti frutti", "yogurtland",
]

# ========= SINGAPORE-SPECIFIC CHAINS =========

SINGAPORE_CHAINS = [
    # Local Fast Food / Casual
    "ya kun", "yakun", "toast box", "killiney", "fun toast",
    "old chang kee", "old changkee", "curry times",
    "chicken rice shop", "the chicken rice shop",
    
    # Local Cafe Chains
    "wang cafe", "ya kun kaya toast", "tong ah eating house",
    "chin mee chin", "heap seng leong",
    
    # Asian Chain Restaurants (SG/Regional)
    "paradise dynasty", "crystal jade", "din tai fung",
    "imperial treasure", "putien", "canton paradise",
    "four seasons", "swensen", "swensen's", "pizza hut",
    "saizeriya", "ajisen ramen", "ippudo", "ramen champion",
    "hokkaido ramen santouka", "tamoya udon", "men-ichi",
    
    # Bubble Tea & Dessert Chains
    "koi", "koi cafe", "liho", "gong cha", "tiger sugar",
    "chicha san chen", "each a cup", "playmade", "bober tea",
    "milksha", "mxc", "r&b tea", "itea", "sharetea",
    "meetfresh", "blackball", "quickly", "mr bean",
    
    # Bakery Chains (SG)
    "breadtalk", "paris baguette", "four leaves", "bengawan solo",
    "sunshine bakery", "cake spade", "barcook bakery",
    
    # Western Fast Casual (SG)
    "stuff'd", "stuffd", "mcdonald's", "burger king", "mos burger",
    "subway", "carl's jr", "popeyes", "texas chicken",
    "long john silver's", "a&w", "wendy's",
    
    # Local Restaurant Chains
    "soup spoon", "the soup spoon", "pastamania", "canadian pizza",
    "spizza", "peperoni pizzeria", "morganfield's", "morganfield",
    "han's", "hans", "delifrance", "délifrance",
    "botak jones", "army stew", "seoul garden", "shaburi",
    "hai di lao", "haidilao", "beauty in the pot",
    "dian xiao er", "jumbo seafood", "no signboard",
    "long beach seafood", "palm beach seafood",
    
    # Halal Chains
    "nasi lemak ayam taliwang", "warong nasi pariaman",
    "hjh maimunah", "zam zam", "victory restaurant",
]

# Hawker centres and food courts
HAWKER_CENTRE_KEYWORDS = [
    "hawker centre", "hawker center", "food centre", "food center",
    "food court", "market & food centre", "kopitiam", "coffee shop",
    "food republic", "food opera", "food junction", "koufu",
]

# Dessert keywords for filtering
DESSERT_KEYWORDS = [
    "ice cream", "gelato", "froyo", "frozen yogurt",
    "dessert bar", "sweet", "cake shop", "cupcake",
    "donut", "doughnut", "candy", "chocolate shop",
]

st.set_page_config(
    page_title="NomNom",
    layout="centered",
)

# === Website Design ===
BASE_CSS = """
<style>
    /* Global font */
    body, .stApp, .block-container, .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #ffffff !important;
    }

    /* Center everything */
    .block-container {
        max-width: 680px !important;
        margin: 0 auto !important;
        text-align: center !important;
        padding-top: 32px !important;
        padding-bottom: 48px !important;
    }

    /* Headers - distinct visual hierarchy */
     h1 {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #ffe066 !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.04em !important;
        line-height: 1 !important;
    }
    h3 { 
        color: #66c2c2 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        margin-top: 0 !important;
    }
    
    /* Section headers with subtle glow effect */
    .section-header {
        font-size: 16px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: #ffd93d !important;
        margin: 32px auto 20px auto !important;
        padding: 12px 24px !important;
        background: linear-gradient(135deg, rgba(255, 217, 61, 0.08) 0%, rgba(255, 217, 61, 0.02) 100%) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 217, 61, 0.2) !important;
        display: table !important;
        text-align: center !important;
    }

    p, label { color: #e5e7eb !important; }

    /* Background */
    .main, .main .block-container {
        background-color: #0a0a0a !important;
    }

    /* Center all inputs */
    div[data-testid="stRadio"],
    div[data-testid="stTextInput"],
    div[data-testid="stSelectbox"] {
        text-align: center !important;
    }
    
    div[data-testid="stRadio"] > label,
    div[data-testid="stTextInput"] > label,
    div[data-testid="stSelectbox"] > label {
        justify-content: center !important;
        text-align: center !important;
        font-weight: 500 !important;
    }

    /* Radio buttons styling */
    div[data-testid="stRadio"] > div {
        justify-content: center !important;
        gap: 16px !important;
    }

    /* Text inputs */
    input[type="text"] {
        text-align: center !important;
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 12px 20px !important;
        font-size: 15px !important;
    }
    input[type="text"]:focus {
        border-color: #ffd93d !important;
        box-shadow: 0 0 0 3px rgba(255, 217, 61, 0.1) !important;
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 12px !important;
    }

    /* All buttons - uniform size and styling */
    div[data-testid="stButton"] {
        text-align: center !important;
        width: 100% !important;
    }
    div[data-testid="stButton"] > button {
        width: 100% !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
        padding: 18px 32px !important;
        margin: 16px auto !important;
        display: block !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        letter-spacing: 0.5px !important;
        background: linear-gradient(135deg, #ffd93d 0%, #ffeb70 100%) !important;
        background-color: #ffd93d !important;
        color: #2d2d2d !important;
        box-shadow: 0 4px 20px rgba(255, 217, 61, 0.4) !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background: linear-gradient(135deg, #ffe066 0%, #fff59d 100%) !important;
        background-color: #ffe066 !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(255, 217, 61, 0.6) !important;
        color: #2d2d2d !important;
    }
    
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button span,
    div[data-testid="stButton"] > button div {
        color: #2d2d2d !important;
        font-weight: 800 !important;
    }

    /* GO button - turquoise (NUCLEAR override for config.toml) */
    button[kind="primary"],
    button.primary,
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stButton"] > button[kind="primary"],
    .stButton > button[kind="primary"],
    section button[kind="primary"],
    [data-testid="stButton"] [kind="primary"] {
        background: linear-gradient(135deg, #66c2c2 0%, #7dd3d3 100%) !important;
        background-color: #66c2c2 !important;
        box-shadow: 0 4px 20px rgba(102, 194, 194, 0.4) !important;
        color: #2d2d2d !important;
        width: 100% !important;
        padding: 18px 32px !important;
        margin: 16px auto !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 800 !important;
        font-size: 16px !important;
    }
    button[kind="primary"]:hover,
    button.primary:hover,
    div[data-testid="stButton"] button[kind="primary"]:hover,
    div[data-testid="stButton"] > button[kind="primary"]:hover,
    .stButton > button[kind="primary"]:hover,
    section button[kind="primary"]:hover,
    [data-testid="stButton"] [kind="primary"]:hover {
        background: linear-gradient(135deg, #7dd3d3 0%, #94e0e0 100%) !important;
        background-color: #7dd3d3 !important;
        box-shadow: 0 8px 30px rgba(102, 194, 194, 0.6) !important;
        color: #2d2d2d !important;
        transform: translateY(-3px) !important;
    }
    button[kind="primary"] p,
    button[kind="primary"] span,
    button[kind="primary"] div,
    div[data-testid="stButton"] > button[kind="primary"] p,
    div[data-testid="stButton"] > button[kind="primary"] span,
    div[data-testid="stButton"] > button[kind="primary"] div {
        color: #2d2d2d !important;
        font-weight: 800 !important;
    }

    /* Sliders - refined look */
    [data-testid="stSlider"] {
        padding: 8px 0 !important;
    }
    [data-testid="stSlider"] .rc-slider-rail { 
        background-color: #1a1a1a !important;
        height: 6px !important;
    }
    [data-testid="stSlider"] .rc-slider-track { 
        background: linear-gradient(90deg, #ffd93d 0%, #ffeb70 100%) !important;
        height: 6px !important;
    }
    [data-testid="stSlider"] .rc-slider-handle {
        border: 3px solid #ffd93d !important;
        background-color: #0a0a0a !important;
        width: 20px !important;
        height: 20px !important;
        margin-top: -7px !important;
        box-shadow: 0 2px 8px rgba(255, 217, 61, 0.4) !important;
    }
    [data-testid="stSlider"] .rc-slider-handle:active,
    [data-testid="stSlider"] .rc-slider-handle:hover,
    [data-testid="stSlider"] .rc-slider-handle:focus {
        border-color: #ffeb70 !important;
        box-shadow: 0 4px 16px rgba(255, 217, 61, 0.6) !important;
    }

    /* Result cards - premium feel */
    .result-card {
        border: 1px solid #1f1f1f !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        margin-bottom: 16px !important;
        background: linear-gradient(135deg, #0f0f0f 0%, #141414 100%) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .result-card:hover {
        border-color: #ffd93d !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 12px 32px rgba(255, 217, 61, 0.15) !important;
        background: linear-gradient(135deg, #141414 0%, #1a1a1a 100%) !important;
    }
    .result-title {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 10px !important;
        letter-spacing: -0.3px !important;
    }
    .result-meta {
        font-size: 14px !important;
        color: #9ca3af !important;
        margin-bottom: 8px !important;
        font-weight: 500 !important;
    }
    .result-badge {
        display: inline-block !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #ffd93d !important;
        background-color: rgba(255, 217, 61, 0.12) !important;
        border: 1px solid rgba(255, 217, 61, 0.2) !important;
        border-radius: 8px !important;
        padding: 6px 12px !important;
        margin-right: 8px !important;
    }

    /* Links in cards */
    .result-card a {
        color: #ffd93d !important;
        text-decoration: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }
    .result-card a:hover {
        color: #ffeb70 !important;
        text-decoration: underline !important;
    }

    /* Section spacers */
    .section-spacer {
        height: 24px;
    }

    /* Smooth fade-in for results */
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
    .results-container {
        animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Success/info messages styling */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 12px !important;
        border-left: 4px solid #ffd93d !important;
    }
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


def autocomplete_places(query: str, region: str = None, max_results: int = 5) -> List[Dict[str, Any]]:
    """Places Autocomplete: get candidate locations."""
    params = {
        "key": API_KEY,
        "input": query,
    }
    if region:
        params["region"] = region
        
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
    search_type: str = "All",
    cuisine_filter: str = "All Cuisines",
) -> List[Dict[str, Any]]:
    """Use Places Nearby Search to get eateries based on type and cuisine filter."""
    
    # Map user selection to Google Places API types
    if search_type == "Bars only":
        place_types = ["bar", "night_club"]
    elif search_type == "Desserts only":
        place_types = ["bakery", "cafe"]
    else:  # "All"
        place_types = ["restaurant", "cafe", "bar"]

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
        
        # Add dessert keyword for desserts only
        if search_type == "Desserts only":
            params["keyword"] = "dessert ice cream gelato cake pastry"

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

def get_chain_blacklist(mode: str) -> List[str]:
    """Get the appropriate chain blacklist based on mode."""
    global_chains = (
        GLOBAL_FAST_FOOD +
        GLOBAL_COFFEE +
        GLOBAL_CASUAL_DINING +
        GLOBAL_ASIAN_CHAINS +
        EUROPEAN_CHAINS +
        MIDDLE_EAST_CHAINS +
        CONVENIENCE_CHAINS +
        GLOBAL_DESSERT_CHAINS
    )
    
    if mode == "Singapore":
        return global_chains + SINGAPORE_CHAINS
    else:  # Global mode
        return global_chains


def filter_and_score_places(
    places: List[Dict[str, Any]],
    min_rating: float,
    min_reviews: int,
    price_filter: str,
    center_lat: float,
    center_lng: float,
    search_type: str,
    mode: str,
) -> List[Dict[str, Any]]:
    """Apply filters and score places - AGGRESSIVE."""

    def haversine_m(lat1, lon1, lat2, lon2) -> float:
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # Get appropriate chain blacklist
    chain_blacklist = get_chain_blacklist(mode)
    
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

        # AGGRESSIVE: Exclude chains based on mode
        if any(k in name for k in chain_blacklist):
            continue
        
        # Exclude obvious centres / markets (mainly for Singapore)
        if mode == "Singapore":
            if any(k in name for k in HAWKER_CENTRE_KEYWORDS):
                continue
        
        # Exclude delivery-only places
        if any(k in name for k in DELIVERY_ONLY_KEYWORDS):
            continue
        
        # AGGRESSIVE: Exclude if it's ONLY meal_delivery or meal_takeaway
        if "meal_delivery" in types and "restaurant" not in types and "cafe" not in types and "bar" not in types:
            continue
        if "meal_takeaway" in types and "restaurant" not in types and "cafe" not in types and "bar" not in types:
            continue
        
        # If searching for food (not desserts/bars), exclude dessert-only places
        if search_type == "All":
            if any(k in name for k in DESSERT_KEYWORDS) and "restaurant" not in types:
                continue
            
        if rating is None or plat is None or plng is None:
            continue
        if rating < min_rating or reviews < min_reviews:
            continue

        # AGGRESSIVE PRICE FILTERING
        if price_filter == "Cheap only (Google 0–1)":
            # Exclude places with missing price data OR price > 1
            if price is None or price > 1:
                continue
        elif price_filter == "Exclude expensive (Google >2)":
            # Exclude places with price > 2 (but allow missing data)
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

# === MODE SELECTION ===
st.markdown('<div class="section-header">Mode</div>', unsafe_allow_html=True)

mode = st.radio(
    "",
    ["Singapore", "Global"],
    index=0,
    label_visibility="collapsed",
    help="Singapore mode: Filters SG + global chains. Global mode: Filters global chains only."
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
        placeholder="e.g. Trastevere, Piazza Navona, Orchard Road",
    )

    if st.button("Search", key="search_places", use_container_width=True):
        q = query.strip()
        if not q:
            st.error("Please enter a location to search.")
        else:
            try:
                # Use region bias for Singapore mode
                region = "sg" if mode == "Singapore" else None
                candidates = autocomplete_places(q, region=region, max_results=5)
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

# Type filter - simplified and more meaningful
search_type = st.selectbox(
    "Type",
    [
        "All",
        "Bars only",
        "Desserts only",
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
                    search_type=search_type,
                    mode=mode,
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
            price_symbols = ["$", "$", "$", "$", "$$"]
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
