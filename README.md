# 🌾 AgroAdvisor TN — AI Farmer Advisory Tool
### Streamlit · Google Gemini 1.5 Flash · Open-Meteo · BCA Final Year Project

> A **production-ready**, bilingual (English/Tamil) agricultural advisory system for Tamil Nadu farmers.  
> **100% free to operate.** No paid APIs. No subscriptions.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌦️ **Live Weather** | Real-time data for all 13 TN districts via Open-Meteo (free, no key) |
| 🛡️ **Resource Guard** | Automatically warns farmers NOT to spray/fertilize if rain >50% or wind >20 km/h |
| 🌾 **Crop & Soil AI** | Gemini recommends best crops based on soil, season, water source & district |
| 🐛 **Pest Diagnosis AI** | Acts as a plant pathologist — suggests free/organic treatments first |
| 🗓️ **Weather Planning AI** | Generates a personalized farm activity schedule |
| 💰 **Schemes Hub** | 6 active TN/Central schemes with eligibility tips in `st.expander` |
| 📅 **Crop Calendar** | Searchable table of 15 crops with sowing/growing/harvest windows |
| 🌐 **Bilingual** | Full English / Tamil toggle in sidebar |
| 🎨 **Nature Theme** | Custom green CSS, no third-party UI components needed |

---

## 🗂️ Project Structure

```
agro-streamlit/
├── app.py                        ← Full Streamlit application (single file)
├── requirements.txt              ← Exact package versions for Python 3.11
├── .streamlit/
│   ├── config.toml               ← Theme (green) + server settings
│   └── secrets.toml              ← YOUR API KEY GOES HERE (never commit)
└── README.md
```

---

## ⚙️ Setup — 5 Steps

### 1. Python 3.11 Check
```bash
python --version   # Must be 3.11.x
```

### 2. Create & activate virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API Key
Open `.streamlit/secrets.toml` and replace the placeholder:
```toml
GEMINI_API_KEY = "AIza..."   # ← paste your real key here
```
**Get a free key (takes 30 seconds):** https://aistudio.google.com/app/apikey  
Free tier: **15 requests/minute, 1 million tokens/day** — more than enough.

### 5. Run the app
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`

---

## 🔑 API Keys Summary

| Service | Key Required? | Cost | Where to Get |
|---|---|---|---|
| **Google Gemini 1.5 Flash** | ✅ Yes | Free (generous tier) | [aistudio.google.com](https://aistudio.google.com/app/apikey) |
| **Open-Meteo Weather** | ❌ No | Free forever | Built-in — no signup |

---

## 🛡️ Resource Guard Logic

The Resource Guard automatically evaluates three farm activities:

| Condition | Spray | Fertilise | Irrigate |
|---|---|---|---|
| Wind > 20 km/h | 🛑 STOP | ✅ OK | ✅ OK |
| Rain prob > 50% | 🛑 STOP | 🛑 STOP | ⏳ WAIT |
| Humidity > 85% | ⚠️ CAUTION | ✅ OK | ✅ OK |
| Rain > 10 mm | 🛑 STOP | 🛑 STOP | ⏸️ SKIP |
| Rain prob 30–50% | ✅ OK | ✅ IDEAL | ✅ OK |

---

## 🌐 Supported Districts

Coimbatore · Erode · Salem · Tiruppur · Namakkal · Madurai · Dindigul ·  
Tirunelveli · Thanjavur · Trichy · Vellore · Tiruvannamalai · Chennai

---

## 📦 Dependencies

```
streamlit==1.35.0           # Web framework
google-generativeai==0.7.2  # Gemini 1.5 Flash AI
httpx==0.27.0               # Async HTTP for Open-Meteo
pandas==2.2.2               # Crop calendar data management
Pillow==10.3.0              # Image support
```

---

## 🔒 Security Notes

- API key stored in `.streamlit/secrets.toml` — accessed via `st.secrets` (never hardcoded)
- Add `.streamlit/secrets.toml` to `.gitignore` before pushing to GitHub
- Weather data cached for 15 minutes (`@st.cache_data(ttl=900)`) to avoid rate limits

---

## 🚀 Deploy to Streamlit Cloud (Free)

1. Push code to a **public** GitHub repo (do NOT include `secrets.toml`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. In **Advanced Settings → Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy** — live URL in 2 minutes, free forever!

---

## 👨‍🎓 Project Info

- **Domain:** AgriTech · Artificial Intelligence · Tamil Nadu Agriculture  
- **Framework:** Streamlit (Python)  
- **AI Engine:** Google Gemini 1.5 Flash  
- **Weather:** Open-Meteo (free, no key)  
- **Language:** Python 3.11  
- **Total Cost to Run:** ₹0 / $0  
