"""
Food Verse AI – Multimodal Food Intelligence Platform
======================================================
FastAPI Application Entrypoint
Unified REST & Multimodal Intelligence Endpoints:
1. Food Recognition & Nutrition (with Health Score)
2. Freshness & Spoilage Detection
3. Restaurant Kitchen Hygiene Monitoring
4. Smart Cooking Assistant (Voice / Text / Vision)
5. Personalized Meal Planning
6. Intelligence Dashboard & System Health
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.config import BASE_DIR, get_gemini_api_key, is_ai_enabled
from backend.models import (
    FoodAnalyzeRequest, FoodAnalyzeResponse,
    FreshnessRequest, FreshnessResponse,
    HygieneAnalyzeRequest, HygieneAnalyzeResponse,
    CookingAssistantRequest, CookingAssistantResponse,
    MealPlanRequest, MealPlanResponse,
    PlatformStatusResponse
)
from backend.services.food_service import analyze_food_image
from backend.services.freshness_service import analyze_freshness
from backend.services.hygiene_service import analyze_kitchen_hygiene
from backend.services.cooking_service import generate_cooking_guidance
from backend.services.meal_plan_service import generate_meal_plan

# Initialize FastAPI application
app = FastAPI(
    title="Food Verse AI – Multimodal Food Intelligence Platform",
    description="Unified AI Platform for Food Recognition, Nutrition, Freshness, Hygiene Monitoring, Cooking, and Meal Planning.",
    version="3.0.0"
)

# Enable Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/status", response_model=PlatformStatusResponse)
def get_system_status():
    """System health and active module status."""
    ai_active = is_ai_enabled()
    return PlatformStatusResponse(
        status="healthy",
        version="3.0.0 (Unified Multimodal Platform)",
        ai_enabled=ai_active,
        mode="Live Multimodal AI (Gemini Vision)" if ai_active else "Mock Demo Mode (Offline)",
        modules=[
            "Food Recognition & Health Score",
            "Visual Freshness & Spoilage",
            "Kitchen Hygiene Monitoring",
            "Smart Cooking Assistant (Voice & Vision)",
            "Personalized Meal Planning",
            "Actionable Intelligence Dashboard"
        ]
    )

@app.post("/api/food/recognize", response_model=FoodAnalyzeResponse)
def endpoint_food_recognize(payload: FoodAnalyzeRequest):
    """Module 1: Food Recognition, Macronutrients & Health Score."""
    if not payload.image:
        raise HTTPException(status_code=400, detail="Food image is required.")
    return analyze_food_image(payload.image, payload.sample_tag or "")

@app.post("/api/food/freshness", response_model=FreshnessResponse)
def endpoint_food_freshness(payload: FreshnessRequest):
    """Module 2: Visual Freshness & Spoilage Detection."""
    if not payload.image:
        raise HTTPException(status_code=400, detail="Image is required for freshness analysis.")
    return analyze_freshness(payload.image, payload.sample_tag or "")

@app.post("/api/hygiene/analyze", response_model=HygieneAnalyzeResponse)
def endpoint_kitchen_hygiene(payload: HygieneAnalyzeRequest):
    """Module 3: Restaurant Kitchen Hygiene & Safety Audit."""
    if not payload.video_or_frame:
        raise HTTPException(status_code=400, detail="Video frame or kitchen image is required.")
    return analyze_kitchen_hygiene(payload.video_or_frame, payload.restaurant_name or "Kitchen Station")

@app.post("/api/cooking/assistant", response_model=CookingAssistantResponse)
def endpoint_cooking_assistant(payload: CookingAssistantRequest):
    """Module 4: Smart Cooking Assistant (Voice / Text / Vision)."""
    return generate_cooking_guidance(
        query_text=payload.query_text or "",
        voice_transcript=payload.voice_transcript or "",
        ingredients_image=payload.ingredients_image or "",
        dietary_preference=payload.dietary_preference or "None"
    )

@app.post("/api/mealplan/generate", response_model=MealPlanResponse)
def endpoint_meal_plan(payload: MealPlanRequest):
    """Module 5: Personalized Adaptive Meal Planning."""
    return generate_meal_plan(
        age=payload.age,
        weight_kg=payload.weight_kg,
        height_cm=payload.height_cm,
        activity_level=payload.activity_level,
        dietary_goal=payload.dietary_goal,
        dietary_restrictions=payload.dietary_restrictions,
        target_calories=payload.target_calories
    )

# Backward compatibility for Phase 1 & 2 client requests
@app.post("/api/analyze")
def endpoint_legacy_analyze(payload: dict):
    image_data = payload.get("image", "")
    sample_tag = payload.get("sampleTag", "") or payload.get("sample_tag", "")
    
    food_res = analyze_food_image(image_data, sample_tag)
    fresh_res = analyze_freshness(image_data, sample_tag)
    
    return {
        "success": True,
        "name": food_res.name,
        "description": food_res.description,
        "nutrition": food_res.nutrition.model_dump(),
        "health_score": food_res.health_score,
        "health_rating": food_res.health_rating,
        "health_insights": food_res.health_insights,
        "freshness": {
            "status": "fresh" if fresh_res.classification == "Fresh" else ("eat_soon" if fresh_res.classification == "Moderately Fresh" else "spoiled"),
            "label": f"{fresh_res.classification} ({fresh_res.shelf_life_estimate})",
            "score": fresh_res.freshness_score,
            "shelf_life": fresh_res.shelf_life_estimate,
            "visual_cues": fresh_res.surface_patterns,
            "storage_tip": fresh_res.storage_recommendation,
            "safety_advisory": fresh_res.safety_advisory
        },
        "is_mock": food_res.is_mock,
        "source_label": food_res.source_label,
        "note": food_res.note
    }

# ---------------------------------------------------------------------------
# Static Files & SPA Routing
# ---------------------------------------------------------------------------
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

# Mount remaining static assets (style.css, app.js, samples)
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")
