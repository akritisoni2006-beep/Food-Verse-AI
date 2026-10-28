# 🍲 Food Verse AI – Multimodal Food Intelligence Platform

Welcome to **Food Verse AI**, an enterprise-grade multimodal food intelligence agent and unified platform designed to analyze food through **Images, Videos, Audio, and Text**.

Powered by a **FastAPI** backend and an interactive **ReactJS** frontend, Food Verse AI provides end-to-end capabilities spanning computer vision, culinary intelligence, kitchen safety, and personalized health.

---

## 🌟 Platform Capabilities (All 10 Core Instructions Implemented)

### 1. Unified Multimodal Platform
Integrates images, kitchen videos, speech/voice audio, and natural language into a single intuitive interface.

### 2. Computer Vision Food Recognition
Automatically identifies dishes and food items from uploaded photos or camera captures using computer vision.

### 3. Nutrition Analysis & Holistic Health Score
Estimates Calories, Protein, Carbohydrates, Total Fat, Dietary Fiber, and computes a comprehensive **Health Score (0–100)** with nutritional grading (e.g., *Grade A+ Superfood* vs *Grade C High Saturated Fat*).

### 4. Visual Freshness & Spoilage Classifier
Evaluates surface patterns, moisture, texture, and oxidation to classify food into:
- 🟢 **Fresh**
- 🟡 **Moderately Fresh (Eat Soon)**
- 🔴 **Spoiled (Unsafe / Discard)**  
Includes estimated shelf life and specific storage recommendations.

### 5. Restaurant Hygiene & Kitchen Safety Monitor
Audits kitchen station frames and video feeds to evaluate:
- **Glove Usage Compliance (%)**
- **Hair-Cap & Beard-Net Adherence (%)**
- **Food Contact Surface Cleanliness (%)**
- **Cross-Contamination Hazard Risk** (Low, Moderate, High)
- Generates immediate corrective safety alerts.

### 6. Smart Cooking Assistant (Voice, Audio, Text, Vision)
- **Voice Queries**: Click the microphone button 🎙️ and speak directly to Chef AI using Web Speech recognition.
- **Vision Queries**: Upload a picture of your refrigerator or pantry to incorporate detected ingredients.
- **Interactive Guidance**: Generates step-by-step recipes with **built-in cooking countdown timers** and chef secrets.

### 7. Personalized Adaptive Meal Planning
Calculates Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE) using the Mifflin-St Jeor formula:
- Supports dietary goals: *Weight Loss*, *Muscle Gain*, *Keto*, *High Protein*, *Diabetic-Friendly (Low Glycemic)*, and *Balanced*.
- Generates 4-meal daily schedules (Breakfast, Lunch, Dinner, Snack) with exact calorie targets and macro splits.
- Recommends customized daily hydration targets.

### 8. Multimodal AI Integration
Combines computer vision, audio processing, and an LLM reasoning engine (Google Gemini 1.5 Flash Vision) with full offline mock fallback support.

### 9. Scalable Full-Stack Architecture
- **Backend**: Built with **FastAPI** and **Uvicorn**, structured with modular services in `backend/services/`.
- **Frontend**: Component-driven **ReactJS** interface with smooth keyframe animations and `prefers-reduced-motion` accessibility.
- **Interactive API Documentation**: Auto-generated Swagger UI available at `/docs`.

### 10. Actionable AI Insights & Dashboards
Consolidated Intelligence Dashboard featuring:
- Key Performance Indicators (KPIs)
- Live Food Safety & Sanitation Alerts feed
- Multimodal AI pipeline flow diagram
- **One-click "Export / Print Executive Report"** feature (`window.print()`).

---

## 📁 Project Architecture

```text
Project/
├── backend/                        # Modular FastAPI Backend
│   ├── __init__.py
│   ├── config.py                   # Environment loader & API settings
│   ├── models.py                   # Pydantic schemas across all 6 modules
│   ├── services/                   # Modular capability services
│   │   ├── __init__.py
│   │   ├── food_service.py         # Food recognition, macros & health score
│   │   ├── freshness_service.py    # Freshness & spoilage classifier
│   │   ├── hygiene_service.py      # Restaurant kitchen video inspection
│   │   ├── cooking_service.py      # Voice/text/vision cooking assistant
│   │   └── meal_plan_service.py    # TDEE calculator & adaptive meal planner
│   └── main.py                     # FastAPI REST app & static file mounting
├── app.py                          # Unified launcher (Uvicorn + FastAPI)
├── app.js                          # React 18 component application
├── index.html                      # HTML5 container & React mounting point
├── style.css                       # Responsive theme, keyframe animations & print CSS
├── .env.example                    # Environment configuration template
├── samples/                        # Quick-test dish images
│   ├── pizza.png
│   ├── burger.png
│   ├── sushi.png
│   └── salad.png
└── README.md                       # Complete platform documentation
```

---

## 🚀 How to Run the Platform

### Step 1: Open Your Terminal
```powershell
cd c:\Users\Lenovo\Downloads\Project
```

### Step 2: Start the FastAPI Server
```powershell
python app.py
```

You will see:
```text
====================================================================
  🍲 Food Verse AI – Multimodal Food Intelligence Platform
====================================================================
  👉 Web Dashboard:    http://localhost:8000
  📖 API Documentation: http://localhost:8000/docs
  ⚡ Backend Engine:    FastAPI + Uvicorn
  💡 AI Engine Status: MOCK DEMO MODE (Default, no key required)
====================================================================
```

### Step 3: Open in Your Browser
- **Web Dashboard**: 👉 **[http://localhost:8000](http://localhost:8000)**
- **Interactive API Swagger Docs**: 👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🔑 Activating Live Multimodal AI (Optional)

The platform works out of the box in **Mock Demo Mode**.

To enable live multimodal vision:
1. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
2. Paste your free Google AI Studio key:
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```
3. Restart `python app.py`. The backend will automatically switch to **Live Multimodal AI**.

---

## 🛑 How to Stop the Server
Press `Ctrl + C` in the terminal where `python app.py` is running.
