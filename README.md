# 🍲 Food Verse AI – Multimodal Food Intelligence Platform

Welcome to **Food Verse AI**, a multimodal food intelligence agent and unified full-stack application designed to analyze food through **Images, Videos, Audio, and Text**.

Powered by a **FastAPI** backend and an interactive **ReactJS** frontend, Food Verse AI provides end-to-end capabilities spanning computer vision, culinary intelligence, kitchen safety, and personalized nutrition.

---

## 📊 Feature Status & Transparency Matrix

The platform is designed with an honest separation between live external AI services, offline deterministic scientific algorithms, and simulated demonstrations:

| Capability / Module | Mode | Implementation Details | Live Key Required? |
| :--- | :---: | :--- | :---: |
| **1. Food Recognition & Nutrition** | **Mock / Demo** *(Live Optional)* | Computes calories, macronutrients, and a holistic Health Score (0–100). Default runs on curated nutritional presets (`samples/`). | **Yes** (Requires valid Gemini Vision key for custom photo identification) |
| **2. Visual Freshness & Spoilage** | **Mock / Demo** *(Live Optional)* | Classifies food as Fresh, Moderately Fresh, or Spoiled with shelf-life estimations and storage guidance. | **Yes** (Requires valid Gemini Vision key for custom photo grading) |
| **3. Restaurant Hygiene Monitor** | **Simulated Demo** | Evaluates kitchen frames against simulated HACCP criteria: glove compliance, hair-cap compliance, surface cleanliness, and cross-contamination alerts. | **No** (Deterministic demonstration audit) |
| **4. Smart Cooking Assistant** | **Functional** | Voice input and text-to-speech synthesis via browser **Web Speech API**; interactive countdown timers per recipe step; curated chef database. | **No** (Browser Web Speech API + internal culinary database) |
| **5. Personalized Meal Planner** | **Fully Functional** | Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the scientifically validated **Mifflin-St Jeor Formula**. Generates 4-meal daily schedules and macro splits. | **No** (100% deterministic scientific calculation) |
| **6. Intelligence Dashboard** | **Presentation Ready** | Live KPI summary, active sanitation alert logs, system status indicator, and one-click Executive Report printing via `window.print()`. | **No** (Client-side interactive dashboard) |

> [!IMPORTANT]
> **AI Status Notice**: Food recognition and freshness detection run in **Mock Demo Mode** out-of-the-box. The application does not claim live computer vision or freshness analysis until configured with a valid Google Gemini API key.

---

## 📁 Project Architecture

```text
Food-Verse-AI/
├── backend/                        # Modular FastAPI Backend
│   ├── __init__.py
│   ├── config.py                   # Environment loader, key validator & AI mode check
│   ├── models.py                   # Pydantic schemas across all 6 modules
│   ├── services/                   # Modular capability services
│   │   ├── __init__.py
│   │   ├── food_service.py         # Food recognition, macros & health score
│   │   ├── freshness_service.py    # Freshness & spoilage classifier
│   │   ├── hygiene_service.py      # Restaurant kitchen video inspection
│   │   ├── cooking_service.py      # Voice/text/vision cooking assistant
│   │   └── meal_plan_service.py    # TDEE calculator & adaptive meal planner
│   └── main.py                     # FastAPI REST app & static file mounting
├── samples/                        # Sample dish assets (Pizza, Burger, Sushi, Salad, Laddu)
│   ├── burger.png
│   ├── laddu.png
│   ├── pizza.png
│   ├── salad.png
│   └── sushi.png
├── app.py                          # Unified launcher (Uvicorn + FastAPI with port auto-select)
├── app.js                          # React 18 component application
├── index.html                      # HTML5 container & React mounting point
├── style.css                       # Responsive theme, keyframe animations & print CSS
├── requirements.txt                # Production Python dependencies
├── Procfile                        # Cloud process file (web worker)
├── render.yaml                     # Render Cloud deployment blueprint
├── .env.example                    # Environment configuration template (safe placeholders)
├── .gitignore                      # Git exclusion rules (protects .env and secrets)
└── README.md                       # Complete platform documentation
```

---

## 🚀 Running Locally

### Prerequisites
- Python 3.10+ (tested with Python 3.11, 3.12, 3.14)
- Web browser (Chrome, Edge, Firefox, or Safari)

### Step 1: Clone the Repository
```bash
git clone https://github.com/akritisoni2006-beep/Food-Verse-AI.git
cd Food-Verse-AI
```

### Step 2: (Optional) Create a Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start the Application
```bash
python app.py
```
*Alternatively, you can run directly with Uvicorn:*
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 5: Open in Your Browser
- **Web Platform**: 👉 **[http://localhost:8000](http://localhost:8000)**
- **Interactive Swagger API Docs**: 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🔑 Activating Live Multimodal AI (Optional)

By default, the platform runs in **Mock Demo Mode** without requiring any API keys.

To connect live Google Gemini Vision:
1. Obtain a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
3. Set your API key in `.env`:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   ```
4. Restart the server (`python app.py`). The header badge will update from **`💡 Mock Demo Mode`** to **`✨ Live Gemini Vision`**.

> [!CAUTION]
> Never commit your `.env` file to GitHub or share your private API keys. The repository `.gitignore` is pre-configured to ignore `.env` files.

---

## ☁️ Cloud Deployment Guide

Food Verse AI is fully packaged for one-click cloud deployment on platforms like **Render**, **Railway**, or **Heroku**.

### Deploying to Render
1. Push your code to your GitHub repository.
2. Sign in to [Render](https://render.com) and click **New > Web Service**.
3. Connect your `Food-Verse-AI` repository.
4. Render will auto-detect [`render.yaml`](render.yaml) or you can configure manually:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. *(Optional)* In the **Environment Variables** tab, add `GEMINI_API_KEY` with your Google AI Studio key.
6. Click **Deploy Web Service**. Render will build the container and provide your live public URL (`https://food-verse-ai.onrender.com`).

### Deploying to Railway / Heroku
- The included [`Procfile`](Procfile) specifies the web worker command:
  ```text
  web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
  ```
- Simply connect the repository to Railway or Heroku; it will automatically install packages from `requirements.txt` and launch the web server.

---

## 🧪 Testing & Verification

Verify backend health and services via the command line:

```bash
# Verify system status endpoint
curl http://localhost:8000/api/status

# Test food analysis endpoint (Mock Mode)
curl -X POST http://localhost:8000/api/food/recognize \
  -H "Content-Type: application/json" \
  -d '{"image": "data:image/png;base64,placeholder", "sample_tag": "pizza"}'
```

---

## 🛑 Stopping the Server
Press `Ctrl + C` in the terminal where the server is running.
