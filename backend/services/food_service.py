"""
Food Verse AI - Food Recognition & Nutrition Service
====================================================
Analyzes food photos to identify dishes, estimate macronutrients,
and calculate a comprehensive nutritional Health Score.
"""

import json
import urllib.request
import urllib.error
import re
from backend.config import get_gemini_api_key
from backend.models import FoodAnalyzeResponse, NutritionFacts

SAMPLE_FOODS = {
    "pizza": {
        "name": "Margherita Pizza",
        "description": "Stone-baked Italian flatbread topped with San Marzano tomato sauce, fresh mozzarella, and aromatic basil leaves.",
        "nutrition": {
            "calories": "260 kcal",
            "serving_size": "1 slice (approx. 100g)",
            "protein": "11g",
            "carbs": "33g",
            "fat": "10g",
            "fiber": "2g"
        },
        "health_score": 72,
        "health_rating": "Grade B (Moderate Balance)",
        "health_insights": [
            "Good source of dairy calcium and lycopene from tomatoes",
            "Refined flour crust contributes moderate simple carbohydrates",
            "Pair with a leafy green salad to boost dietary fiber intake"
        ]
    },
    "burger": {
        "name": "Classic Cheeseburger",
        "description": "Grilled seasoned beef patty with melted cheddar cheese, crisp lettuce, ripe tomatoes, and savory sauce on a brioche bun.",
        "nutrition": {
            "calories": "535 kcal",
            "serving_size": "1 burger (approx. 220g)",
            "protein": "30g",
            "carbs": "40g",
            "fat": "28g",
            "fiber": "3g"
        },
        "health_score": 64,
        "health_rating": "Grade C (High Protein / Moderate Saturated Fat)",
        "health_insights": [
            "High biological value protein for muscle synthesis (30g)",
            "Contains saturated fats from beef patty and cheddar cheese",
            "Opt for a whole-grain bun or lettuce wrap for lower refined carbohydrates"
        ]
    },
    "sushi": {
        "name": "Salmon Nigiri & Maki Combo",
        "description": "Fresh Atlantic salmon over seasoned vinegared sushi rice with nori seaweed and avocado rolls.",
        "nutrition": {
            "calories": "380 kcal",
            "serving_size": "6 pieces (approx. 200g)",
            "protein": "18g",
            "carbs": "55g",
            "fat": "7g",
            "fiber": "2g"
        },
        "health_score": 88,
        "health_rating": "Grade A (Nutrient Dense)",
        "health_insights": [
            "Rich in cardiovascular-protective Omega-3 fatty acids (EPA/DHA)",
            "Lean protein source with low saturated fat content",
            "Seaweed provides essential iodine and micronutrients"
        ]
    },
    "salad": {
        "name": "Mediterranean Garden Salad",
        "description": "Vibrant mixed greens, cucumbers, cherry tomatoes, and red onions tossed with cold-pressed extra-virgin olive oil.",
        "nutrition": {
            "calories": "150 kcal",
            "serving_size": "1 bowl (approx. 180g)",
            "protein": "4g",
            "carbs": "12g",
            "fat": "10g",
            "fiber": "4g"
        },
        "health_score": 96,
        "health_rating": "Grade A+ (Superfood / Antioxidant Rich)",
        "health_insights": [
            "High dietary fiber promotes gut microbiome health",
            "Extra virgin olive oil supplies monounsaturated fatty acids",
            "Abundant vitamins A, C, and K with zero added refined sugars"
        ]
    },
    "laddu": {
        "name": "Traditional Indian Motichoor / Besan Laddu",
        "description": "A golden Indian delicacy prepared with roasted gram flour (besan), pure desi ghee, fragrant cardamom, and roasted nuts.",
        "nutrition": {
            "calories": "185 kcal",
            "serving_size": "1 piece (approx. 45g)",
            "protein": "3.5g",
            "carbs": "24g",
            "fat": "9g",
            "fiber": "1.2g"
        },
        "health_score": 70,
        "health_rating": "Grade B (Festive Delicacy / Healthy Ghee Fats)",
        "health_insights": [
            "Gram flour (besan) provides plant-based protein and iron",
            "Pure desi ghee provides fat-soluble vitamins (A, D, E) and butyric acid",
            "High energy density — optimal as a festive treat or pre-workout energy"
        ]
    }
}

FALLBACK_FOOD = {
    "name": "Artisan Harvest Dish (Demo Result)",
    "description": "A wholesome culinary plate prepared with mixed produce, balanced seasonings, and healthy proteins.",
    "nutrition": {
        "calories": "320 kcal",
        "serving_size": "1 portion (approx. 200g)",
        "protein": "14g",
        "carbs": "38g",
        "fat": "12g",
        "fiber": "5g"
    },
    "health_score": 82,
    "health_rating": "Grade B+ (Well Balanced)",
    "health_insights": [
        "Balanced distribution of macronutrients suitable for active lifestyles",
        "Provides dietary fiber and natural micronutrients",
        "Sample estimation: Configure GEMINI_API_KEY in .env for custom AI vision analysis"
    ]
}

def analyze_food_image(image_data: str, sample_tag: str = "") -> FoodAnalyzeResponse:
    api_key = get_gemini_api_key()

    # If no API key is present, use rich Mock Intelligence
    if not api_key:
        tag = (sample_tag or "").lower().strip()
        
        # Check if sample tag or image matches known items
        data = SAMPLE_FOODS.get(tag)
        if not data:
            # Check if laddu or sweet keyword in tag
            if "laddu" in tag or "ladoo" in tag or "sweet" in tag:
                data = SAMPLE_FOODS["laddu"]
            else:
                data = FALLBACK_FOOD

        return FoodAnalyzeResponse(
            success=True,
            name=data["name"],
            description=data["description"],
            nutrition=NutritionFacts(**data["nutrition"]),
            health_score=data["health_score"],
            health_rating=data["health_rating"],
            health_insights=data["health_insights"],
            is_mock=True,
            source_label="Mock Demo Result",
            note="Running in Mock Mode. Set GEMINI_API_KEY in .env for live Gemini Vision analysis."
        )

    # Live AI analysis with Gemini Vision
    try:
        header, b64_string = image_data.split(",", 1) if "," in image_data else ("", image_data)
        mime_match = re.search(r"data:([^;]+);base64", header)
        mime_type = mime_match.group(1) if mime_match else "image/jpeg"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = (
            "You are a computer vision culinary scientist. Identify the food in this photo, provide estimated nutritional facts, "
            "and compute a holistic Health Score (0 to 100) and Health Rating (e.g. Grade A, Grade B, Grade C).\n"
            "Respond ONLY with a JSON object in this schema:\n"
            "{\n"
            '  "name": "Dish name",\n'
            '  "description": "Short culinary summary",\n'
            '  "nutrition": {\n'
            '    "calories": "Estimated calories (e.g. 350 kcal)",\n'
            '    "serving_size": "Estimated serving size (e.g. 1 bowl)",\n'
            '    "protein": "Protein in grams (e.g. 20g)",\n'
            '    "carbs": "Carbohydrates in grams (e.g. 45g)",\n'
            '    "fat": "Fat in grams (e.g. 10g)",\n'
            '    "fiber": "Dietary fiber (e.g. 4g)"\n'
            "  },\n"
            '  "health_score": 85,\n'
            '  "health_rating": "Grade A (Nutrient Rich)",\n'
            '  "health_insights": ["Insight 1", "Insight 2", "Insight 3"]\n'
            "}\n"
            "Do NOT include markdown formatting."
        )

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime_type, "data": b64_string}}
                ]
            }],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            text = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            parsed = json.loads(text)

            return FoodAnalyzeResponse(
                success=True,
                name=parsed.get("name", "Identified Dish"),
                description=parsed.get("description", "A freshly prepared culinary item."),
                nutrition=NutritionFacts(**parsed.get("nutrition", FALLBACK_FOOD["nutrition"])),
                health_score=parsed.get("health_score", 80),
                health_rating=parsed.get("health_rating", "Grade B"),
                health_insights=parsed.get("health_insights", ["Healthy whole-food ingredients detected."]),
                is_mock=False,
                source_label="Live AI Analysis (Gemini Vision)"
            )
    except Exception as e:
        return FoodAnalyzeResponse(
            success=True,
            name=FALLBACK_FOOD["name"],
            description=f"Fallback result (AI connection note: {str(e)[:60]}).",
            nutrition=NutritionFacts(**FALLBACK_FOOD["nutrition"]),
            health_score=FALLBACK_FOOD["health_score"],
            health_rating=FALLBACK_FOOD["health_rating"],
            health_insights=FALLBACK_FOOD["health_insights"],
            is_mock=True,
            source_label="Fallback Mock Mode",
            note=f"AI connection failed: {str(e)}. Showing fallback estimation."
        )
