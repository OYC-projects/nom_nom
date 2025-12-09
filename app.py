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
