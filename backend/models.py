"""
Food Verse AI - Pydantic Data Models
====================================
Defines typed request and response schemas across all multimodal modules.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Module 1: Food Recognition & Nutrition ---
class NutritionFacts(BaseModel):
    calories: str
    serving_size: str
    protein: str
    carbs: str
    fat: str
    fiber: str

class FoodAnalyzeRequest(BaseModel):
    image: str
    sample_tag: Optional[str] = ""

class FoodAnalyzeResponse(BaseModel):
    success: bool
    name: str
    description: str
    nutrition: NutritionFacts
    health_score: int
    health_rating: str  # e.g., "Grade A (Excellent)"
    health_insights: List[str]
    is_mock: bool
    source_label: str
    note: Optional[str] = None

# --- Module 2: Freshness & Spoilage ---
class FreshnessRequest(BaseModel):
    image: str
    sample_tag: Optional[str] = ""

class FreshnessResponse(BaseModel):
    success: bool
    food_name: str
    classification: str  # "Fresh", "Moderately Fresh", "Spoiled"
    freshness_score: int  # 0 to 100
    shelf_life_estimate: str
    color_analysis: str
    texture_analysis: str
    discoloration_risk: str
    surface_patterns: List[str]
    storage_recommendation: str
    safety_advisory: str
    is_mock: bool

# --- Module 3: Restaurant Hygiene Monitor ---
class HygieneAnalyzeRequest(BaseModel):
    video_or_frame: str  # base64 image or video data
    restaurant_name: Optional[str] = "Kitchen Station #1"

class HygieneMetric(BaseModel):
    name: str
    compliance_percent: int
    status: str  # "Compliant", "Needs Attention", "Violation"
    details: str

class HygieneAnalyzeResponse(BaseModel):
    success: bool
    station_name: str
    overall_sanitation_score: int  # 0 to 100
    inspection_grade: str  # "Grade A", "Grade B", "Critical Audit"
    metrics: List[HygieneMetric]
    glove_compliance: int
    hair_cap_compliance: int
    cross_contamination_risk: str  # "Low", "Moderate", "High"
    cleanliness_score: int
    detected_violations: List[str]
    actionable_recommendations: List[str]
    timestamp: str

# --- Module 4: Smart Cooking Assistant ---
class CookingAssistantRequest(BaseModel):
    query_text: Optional[str] = ""
    voice_transcript: Optional[str] = ""
    ingredients_image: Optional[str] = ""
    dietary_preference: Optional[str] = "None"

class CookingStep(BaseModel):
    step_number: int
    instruction: str
    timer_minutes: Optional[int] = 0
    technique_tip: Optional[str] = ""

class CookingAssistantResponse(BaseModel):
    success: bool
    recipe_name: str
    cuisine: str
    prep_time: str
    cook_time: str
    difficulty: str  # "Easy", "Intermediate", "Advanced"
    servings: int
    ingredients: List[str]
    steps: List[CookingStep]
    chef_secret: str
    nutrition_per_serving: str

# --- Module 5: Personalized Meal Planning ---
class MealPlanRequest(BaseModel):
    age: int = 28
    weight_kg: float = 70.0
    height_cm: float = 175.0
    activity_level: str = "Moderately Active"  # Sedentary, Lightly Active, Moderately Active, Very Active
    dietary_goal: str = "Weight Loss"  # "Weight Loss", "Muscle Gain", "Keto", "High Protein", "Diabetic-Friendly", "Balanced"
    dietary_restrictions: List[str] = []
    target_calories: Optional[int] = None

class MealItem(BaseModel):
    meal_type: str  # "Breakfast", "Lunch", "Dinner", "Snack"
    dish_name: str
    calories: int
    macros: str  # e.g. "P: 25g | C: 40g | F: 12g"
    benefits: str
    prep_time: str

class MealPlanResponse(BaseModel):
    success: bool
    daily_calorie_target: int
    macro_distribution: Dict[str, str]
    plan_title: str
    dietary_goal: str
    meals: List[MealItem]
    hydration_target: str
    coaching_tips: List[str]

# --- Module 6: Intelligence Dashboard / Status ---
class PlatformStatusResponse(BaseModel):
    status: str
    version: str
    ai_enabled: bool
    mode: str
    modules: List[str]
