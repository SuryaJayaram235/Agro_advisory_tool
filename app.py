"""
╔══════════════════════════════════════════════════════════════════════╗
║  AgroAdvisor TN — Farmer Advisory Tool for Tamil Nadu              ║
║  Built with Streamlit · Gemini 1.5 Flash · Open-Meteo              ║
║  BCA Final Year Project — 100% Free to Operate                     ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import httpx
import pandas as pd
import google.generativeai as genai
from datetime import datetime
import json

# ══════════════════════════════════════════════════════════════════════
#  PAGE CONFIG  (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgroAdvisor TN | விவசாயி உதவியாளர்",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  CUSTOM CSS — Nature-Inspired Theme
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;600&display=swap');

/* ── Global ─────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Helvetica Neue', Arial, sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: #f5f7f2; }

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1c4a0a 0%, #27500A 60%, #3B6D11 100%); }
[data-testid="stSidebar"] * { color: #e8f5e9 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label { color: #C0DD97 !important; font-size: 0.78rem; letter-spacing: 0.05em; text-transform: uppercase; }
[data-testid="stSidebar"] [data-baseweb="select"] > div { background: rgba(255,255,255,0.1) !important; border-color: rgba(255,255,255,0.2) !important; color: white !important; }
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] span { border-color: #C0DD97 !important; }

/* ── Top Banner ──────────────────────────────────────── */
.app-header { background: linear-gradient(135deg, #1c4a0a 0%, #27500A 60%, #3B6D11 100%); padding: 1rem 1.5rem; border-radius: 14px; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 4px 20px rgba(39,80,10,0.25); }
.app-header h1 { color: white; font-size: 1.5rem; font-weight: 700; margin: 0; }
.app-header p  { color: #C0DD97; font-size: 0.8rem; margin: 0; font-family: 'Noto Serif Tamil', sans-serif; }

/* ── Metric Cards ────────────────────────────────────── */
.metric-card { background: white; border-radius: 12px; padding: 0.9rem 1rem; border: 1px solid #e8f0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center; }
.metric-card .val { font-size: 1.5rem; font-weight: 700; color: #0F6E56; }
.metric-card .lbl { font-size: 0.72rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }

/* ── Section Cards & Alerts ──────────────────────────── */
.section-card { background: white; border-radius: 14px; padding: 1.2rem 1.4rem; border: 1px solid #e8f0e0; margin-bottom: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
.alert-red { background: #fef2f2; border: 1.5px solid #fca5a5; border-radius: 10px; padding: 0.9rem 1.1rem; color: #7f1d1d; font-weight: 500; }
.alert-caution { background: #fffbeb; border: 1.5px solid #fcd34d; border-radius: 10px; padding: 0.9rem 1.1rem; color: #78350f; font-weight: 500; }

/* ── Resource Guard ──────────────────────────────────── */
.rg-card { background: linear-gradient(135deg, #f0fdf4, #e6f7f4); border: 1.5px solid #86efac; border-radius: 12px; padding: 1rem 1.2rem; }
.rg-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #d1fae5; }
.rg-row:last-child { border-bottom: none; padding-bottom: 0; }
.badge-ok     { background: #d1fae5; color: #065f46; padding: 3px 12px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; }
.badge-caution{ background: #fef3c7; color: #92400e; padding: 3px 12px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; }
.badge-stop   { background: #fee2e2; color: #7f1d1d; padding: 3px 12px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; }

/* ── Scheme Cards ────────────────────────────────────── */
.scheme-badge { padding: 2px 10px; border-radius: 999px; font-size: 0.72rem; font-weight: 700; }
.scheme-badge-state  { background: #dbeafe; color: #1e3a8a; }
.scheme-badge-free   { background: #d1fae5; color: #065f46; }
.scheme-badge-bank   { background: #f3e8ff; color: #4c1d95; }

/* ── AI Response Box & Pest Risk Bar ─────────────────── */
.ai-response { background: #f8fbf5; border: 1px solid #c6e8b0; border-radius: 12px; padding: 1rem 1.2rem; line-height: 1.8; font-size: 0.9rem; color: #1a2e1a; }
.risk-bar-wrap { margin-top: 0.5rem; }
.risk-bar-track { background: #f1f5e8; border-radius: 4px; height: 10px; overflow: hidden; }
.risk-bar-fill  { height: 100%; border-radius: 4px; transition: width 0.6s; }

/* ── Calendar Table ──────────────────────────────────── */
.cal-sow     { background: #1D9E75; color: white; border-radius: 3px; padding:2px 4px; font-size:0.7rem; }
.cal-grow    { background: #C0DD97; color: #27500A; border-radius: 3px; padding:2px 4px; font-size:0.7rem; }
.cal-harvest { background: #EF9F27; color: white; border-radius: 3px; padding:2px 4px; font-size:0.7rem; }
.cal-nursery { background: #9FE1CB; color: #0F6E56; border-radius: 3px; padding:2px 4px; font-size:0.7rem; }

/* ── Tabs & Buttons ──────────────────────────────────── */
[data-baseweb="tab-list"] { background: #eef4e8; border-radius: 10px; padding: 4px; gap: 4px; }
[data-baseweb="tab"]       { border-radius: 8px !important; font-weight: 600 !important; font-size: 0.85rem !important; }
[aria-selected="true"]     { background: #3B6D11 !important; color: white !important; }
.stButton > button { background: linear-gradient(135deg, #2d6a4f, #52b788) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; padding: 0.55rem 1.4rem !important; box-shadow: 0 3px 12px rgba(45,106,79,0.3) !important; transition: all 0.2s !important; }
.stButton > button:hover { filter: brightness(1.08) !important; transform: translateY(-1px) !important; }
[data-baseweb="input"] > div, [data-baseweb="textarea"] > div, [data-baseweb="select"] > div { border-radius: 8px !important; border-color: #c6e8b0 !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-thumb { background: #86efac; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
#  CONSTANTS & DATA
# ══════════════════════════════════════════════════════════════════════
DISTRICTS: dict[str, dict] = {
    "Coimbatore": {"lat": 11.0168, "lon": 76.9558, "zone": "western"},
    "Erode":       {"lat": 11.3410, "lon": 77.7172, "zone": "western"},
    "Salem":       {"lat": 11.6643, "lon": 78.1460, "zone": "western"},
    "Tiruppur":    {"lat": 11.1085, "lon": 77.3411, "zone": "western"},
    "Namakkal":    {"lat": 11.2189, "lon": 78.1674, "zone": "western"},
    "Madurai":     {"lat": 9.9252,  "lon": 78.1198, "zone": "south"},
    "Dindigul":    {"lat": 10.3624, "lon": 77.9695, "zone": "south"},
    "Tirunelveli": {"lat": 8.7139,  "lon": 77.7567, "zone": "south"},
    "Thanjavur":   {"lat": 10.7870, "lon": 79.1378, "zone": "delta"},
    "Trichy":      {"lat": 10.7905, "lon": 78.7047, "zone": "delta"},
    "Vellore":     {"lat": 12.9165, "lon": 79.1325, "zone": "north"},
    "Tiruvannamalai": {"lat": 12.2253, "lon": 79.0747, "zone": "north"},
    "Chennai":     {"lat": 13.0827, "lon": 80.2707, "zone": "north"},
}

SOIL_TYPES = ["Red Soil / சிவப்பு மண்", "Black Cotton Soil / களிமண்", "Sandy Loam / மணல் கலப்பு மண்", "Clay / களி மண்", "Alluvial / வண்டல் மண்"]
GROWTH_STAGES = ["Seedling / நாற்று நிலை", "Vegetative / வளர்ச்சி நிலை", "Flowering / பூக்கும் நிலை", "Fruiting / காய்க்கும் நிலை", "Harvesting / அறுவடை நிலை"]
WATER_SOURCES = ["Borewell / ஆழ்துளை கிணறு", "Canal / கால்வாய்", "Rainwater / மழைநீர்", "Open well / திறந்த கிணறு", "Drip Irrigation / சொட்டு நீர்"]
SEASONS = ["Kharif (Jun–Sep) / காரிஃப்", "Rabi (Oct–Jan) / ரபி", "Summer (Feb–May) / கோடை"]

SCHEMES = [
    {"name": "PM-KISAN", "name_ta": "நேரடி வருமான ஆதரவு", "desc": "₹6,000/year directly to farmers' bank accounts.", "link": "pmkisan.gov.in", "badge": "Central", "badge_class": "scheme-badge scheme-badge-state", "tip": "Register at nearest CSC with Aadhaar."},
    {"name": "TN Crop Insurance — PMFBY", "name_ta": "பயிர் காப்பீடு திட்டம்", "desc": "Insurance covering losses from drought, flood, and pest.", "link": "agri.tn.gov.in", "badge": "State + Central", "badge_class": "scheme-badge", "tip": "Premium is 1.5% for Kharif. Apply before sowing."},
    {"name": "Kisan Credit Card (KCC)", "name_ta": "கிசான் கிரெடிட் கார்டு", "desc": "Crop credit at 4% effective interest for seeds & fertilizers.", "link": "cooperative banks", "badge": "Banking", "badge_class": "scheme-badge scheme-badge-bank", "tip": "Limit up to ₹3 lakhs. Renew annually."},
]

CROP_CALENDAR = [
    {"Crop": "Paddy (Kuruvai)", "Type": "Cereal", "Zone": "Delta", "Sow": "Jun–Jul", "Grow": "Jul–Sep", "Harvest": "Oct", "Tip": "SRI method cuts water by 30%."},
    {"Crop": "Paddy (Samba)", "Type": "Cereal", "Zone": "Delta", "Sow": "Aug–Sep", "Grow": "Sep–Dec", "Harvest": "Jan–Feb", "Tip": "Main season paddy. Use neem oil for BPH."},
    {"Crop": "Maize", "Type": "Cereal", "Zone": "Western", "Sow": "Jun, Nov", "Grow": "Jun–Aug, Nov–Jan", "Harvest": "Aug, Feb", "Tip": "Intercrop with cowpea."},
    {"Crop": "Sugarcane", "Type": "Cash", "Zone": "Western", "Sow": "Jan–Feb", "Grow": "Mar–Nov", "Harvest": "Dec", "Tip": "Drip irrigation mandatory."},
]

# ══════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════
if "lang" not in st.session_state: st.session_state.lang = "en"
if "district" not in st.session_state: st.session_state.district = "Coimbatore"
if "weather" not in st.session_state: st.session_state.weather = None

# ══════════════════════════════════════════════════════════════════════
#  AI ADVISOR (CACHED + GROQ FALLBACK)
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=86400, show_spinner=False)
def get_ai_advisory(system_prompt: str, user_prompt: str) -> str:
    """
    Call Gemini API wisely. Caches exact identical requests for 24 hours.
    Seamlessly falls back to Groq Llama 3.1 if Gemini free tier quota is exceeded.
    """
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key:
            return "⚠️ **API key not configured.** Please add GEMINI_API_KEY to your secrets."
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_prompt)
        response = model.generate_content(
            user_prompt,
            generation_config=genai.GenerationConfig(temperature=0.7, max_output_tokens=700),
        )
        return response.text.strip()
        
    except Exception as e:
        err = str(e).lower()
        if "quota" in err or "rate" in err or "429" in err or "exhausted" in err:
            # GROQ Llama 3.1 Fallback strategy activated
            try:
                from groq import Groq
                groq_key = st.secrets.get("GROQ_API_KEY")
                if not groq_key:
                    return "⚠️ **Gemini API quota exceeded** (15 req/min). Please wait 60 seconds."
                
                client = Groq(api_key=groq_key)
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    max_tokens=700,
                )
                return chat_completion.choices[0].message.content.strip()
            except ImportError:
                return "⚠️ **Gemini API quota exceeded**. Add `groq` to requirements.txt to enable the Llama 3.1 fallback."
            except Exception as groq_e:
                return "⚠️ **API quota exceeded on both Gemini and Groq.** Please try again shortly."
        
        return f"⚠️ **AI service error:** {str(e)}"

# ══════════════════════════════════════════════════════════════════════
#  WEATHER SERVICE
# ══════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=900)
def fetch_weather(district: str) -> dict | None:
    if district not in DISTRICTS: return None
    loc = DISTRICTS[district]
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": loc["lat"], "longitude": loc["lon"],
                    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,rain,wind_speed_10m,cloud_cover,precipitation_probability",
                    "timezone": "Asia/Kolkata",
                },
            )
            resp.raise_for_status()
            c = resp.json()["current"]
            return {
                "temp": c.get("temperature_2m", 0), "feels": c.get("apparent_temperature", 0),
                "humidity": c.get("relative_humidity_2m", 0), "rain": c.get("rain", 0),
                "wind": c.get("wind_speed_10m", 0), "cloud": c.get("cloud_cover", 0),
                "precip_prob": c.get("precipitation_probability", 0),
                "district": district, "fetched_at": datetime.now().strftime("%H:%M"),
            }
    except Exception as e:
        return {"error": str(e)}

def weather_description(w: dict) -> str:
    if not w or "error" in w: return "weather data unavailable"
    return f"{w['temp']}°C, humidity {w['humidity']}%, wind {w['wind']} km/h, rain {w['rain']} mm, precipitation probability {w['precip_prob']}%"

def compute_resource_guard(w: dict) -> dict:
    if not w or "error" in w: return None
    result = {}
    
    # Spray
    if w["wind"] > 20: result["spray"] = {"status": "STOP", "badge": "badge-stop", "reason": "High wind — drift risk", "savings": "💰 Save ₹200–500", "emoji": "🛑"}
    elif w["precip_prob"] > 50 or w["rain"] > 2: result["spray"] = {"status": "STOP", "badge": "badge-stop", "reason": "Rain likely — wash off risk", "savings": "💰 Save chemicals", "emoji": "🛑"}
    else: result["spray"] = {"status": "OK TO SPRAY", "badge": "badge-ok", "reason": "Good conditions.", "savings": "", "emoji": "✅"}

    # Fertilise
    if w["precip_prob"] > 60 or w["rain"] > 5: result["fertilise"] = {"status": "STOP", "badge": "badge-stop", "reason": "Heavy rain — leaching risk", "savings": "💰 Save urea", "emoji": "🛑"}
    else: result["fertilise"] = {"status": "OK", "badge": "badge-ok", "reason": "Conditions acceptable.", "savings": "", "emoji": "✅"}

    # Irrigate
    if w["rain"] > 10: result["irrigate"] = {"status": "SKIP", "badge": "badge-caution", "reason": "Soil saturated", "savings": "💧 Save water", "emoji": "⏸️"}
    else: result["irrigate"] = {"status": "OK", "badge": "badge-ok", "reason": "Irrigate as scheduled.", "savings": "", "emoji": "✅"}
    
    return result

def compute_pest_risk(w: dict) -> tuple:
    if not w or "error" in w: return 0, "Unknown"
    score = (w.get("humidity",0) >= 80) * 30 + (20 <= w.get("temp",25) <= 30) * 20
    score = min(100, score)
    return score, "CRITICAL" if score >= 75 else "HIGH" if score >= 50 else "LOW"

# ══════════════════════════════════════════════════════════════════════
#  UI LAYOUT
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🌾 AgroAdvisor TN")
    lang_choice = st.radio("Language", ["English", "தமிழ்"], horizontal=True)
    st.session_state.lang = "en" if lang_choice == "English" else "ta"
    
    district = st.selectbox("📍 District", list(DISTRICTS.keys()), index=list(DISTRICTS.keys()).index(st.session_state.district))
    if district != st.session_state.district:
        st.session_state.district = district
        st.session_state.weather = None
        st.rerun()

    if st.button("↻ Refresh Weather", use_container_width=True):
        fetch_weather.clear()
        st.session_state.weather = None

    if st.session_state.weather is None:
        with st.spinner("Fetching weather…"):
            st.session_state.weather = fetch_weather(st.session_state.district)

    w = st.session_state.weather
    if w and "error" not in w:
        st.markdown(f"<div style='background:rgba(255,255,255,0.1);padding:1rem;border-radius:10px;'>{w['temp']}°C | 💧 {w['humidity']}%</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="app-header">
    <div style="font-size:2.5rem">🌾</div>
    <div><h1>Farmer Advisory Tool</h1><p>{st.session_state.district}, Tamil Nadu</p></div>
</div>
""", unsafe_allow_html=True)

w = st.session_state.weather
tabs = st.tabs(["🌾 Crop & Soil", "🐛 Pest & Disease", "🌦️ Weather Plan", "💰 Schemes", "📅 Calendar"])

# ── TAB 1 ──
with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        c_soil = st.selectbox("Soil Type", SOIL_TYPES)
        c_season = st.selectbox("Season", SEASONS)
        c_land = st.number_input("Land Size (acres)", 0.5, 100.0, 2.0, 0.5)
    with col2:
        c_water = st.selectbox("Water Source", WATER_SOURCES)
        c_prev = st.text_input("Previous Crop", placeholder="e.g. Paddy")
        c_concern = st.text_area("Specific Concern", height=100)

    if st.button("🌱 Get AI Crop Recommendation", use_container_width=True):
        wx_ctx = weather_description(w)
        sys_p = "You are an expert agricultural advisor for Tamil Nadu. Recommend crops suited for local conditions. Prioritize low-cost, high-return crops."
        usr_p = f"District: {st.session_state.district}\nSoil: {c_soil}\nSeason: {c_season}\nLand: {c_land} ac\nWater: {c_water}\nPrev: {c_prev}\nConcern: {c_concern}\nWeather: {wx_ctx}"
        with st.spinner("🤖 AI is analyzing..."):
            st.markdown(f'<div class="ai-response">{get_ai_advisory(sys_p, usr_p)}</div>', unsafe_allow_html=True)

# ── TAB 2 ──
with tabs[1]:
    col1, col2 = st.columns(2)
    with col1:
        p_crop = st.text_input("Affected Crop", placeholder="e.g. Tomato")
        p_stage = st.selectbox("Growth Stage", GROWTH_STAGES)
    with col2:
        p_area = st.selectbox("Area Affected", ["Less than 10%", "10–30%", "30–60%", "More than 60%"])
    
    p_symptoms = st.text_area("Symptoms Observed", height=110)

    if st.button("🔍 Diagnose & Treat", use_container_width=True):
        if not p_symptoms.strip():
            st.warning("⚠️ Please describe the symptoms before requesting a diagnosis.")
        else:
            wx_ctx = weather_description(w)
            sys_p = "You are a plant pathologist in Tamil Nadu. Prioritize CHEAP biological/organic treatments. Identify the pest/disease."
            usr_p = f"Crop: {p_crop}\nStage: {p_stage}\nSymptoms: {p_symptoms}\nArea: {p_area}\nDistrict: {st.session_state.district}\nWeather: {wx_ctx}"
            with st.spinner("🔍 Diagnosing..."):
                st.markdown(f'<div class="ai-response">{get_ai_advisory(sys_p, usr_p)}</div>', unsafe_allow_html=True)

# ── TAB 3 ──
with tabs[2]:
    if w and "error" not in w:
        rg = compute_resource_guard(w)
        st.markdown('<div class="rg-card">', unsafe_allow_html=True)
        for key in ["spray", "fertilise", "irrigate"]:
            item = rg[key]
            st.markdown(f"<div class='rg-row'><div><strong>{key.title()}</strong><br><small>{item['reason']}</small></div><span class='{item['badge']}'>{item['status']}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4 ──
with tabs[3]:
    scheme_query = st.text_area("Ask about a specific scheme…", height=90)
    if st.button("💡 Ask AI Advisor", use_container_width=True):
        if not scheme_query.strip():
            st.info("⚠️ Please type a specific question about a scheme before asking the AI.")
        else:
            sys_p = "You are a government scheme advisor for Tamil Nadu farmers. Know all central and state agricultural schemes 2024–2025. Explain eligibility simply."
            with st.spinner("💡 Searching scheme info..."):
                st.markdown(f'<div class="ai-response">{get_ai_advisory(sys_p, scheme_query)}</div>', unsafe_allow_html=True)

# ── TAB 5 ──
with tabs[4]:
    st.dataframe(pd.DataFrame(CROP_CALENDAR), use_container_width=True)