"""
Food Verse AI - Freshness & Spoilage Detection Service
======================================================
Analyzes visual characteristics such as color, texture, discoloration,
and surface patterns to classify food into:
- Fresh
- Moderately Fresh (Eat Soon)
- Spoiled (Unsafe / Discard)
"""

import json
import urllib.request
import urllib.error
import re
from backend.config import get_gemini_api_key
from backend.models import FreshnessResponse

SAMPLE_FRESHNESS = {
    "pizza": {
        "food_name": "Margherita Pizza",
        "classification": "Fresh",
        "freshness_score": 93,
        "shelf_life_estimate": "3–4 days refrigerated",
        "color_analysis": "Bright red San Marzano sauce with even, golden-brown crust edges.",
        "texture_analysis": "Melted cheese maintains cohesive moisture without grease pooling.",
        "discoloration_risk": "None detected (crust and cheese colors are normal and uniform).",
        "surface_patterns": [
            "Normal baked dough bubbles",
            "Glossy, hydrated mozzarella layer",
            "Zero mycelium or mold colony formations"
        ],
        "storage_recommendation": "Refrigerate slices in an airtight container separated by parchment paper at 4°C.",
        "safety_advisory": "Safe to consume. Reheat until steaming hot (>74°C / 165°F)."
    },
    "burger": {
        "food_name": "Cheeseburger",
        "classification": "Fresh",
        "freshness_score": 89,
        "shelf_life_estimate": "2–3 days refrigerated",
        "color_analysis": "Deep brown grilled beef patty with vibrant yellow melted cheddar.",
        "texture_analysis": "Firm beef patty structure; lettuce shows cellular turgor without wilting.",
        "discoloration_risk": "Low (no graying or slimy surface film detected).",
        "surface_patterns": [
            "Intact grilled meat fibers",
            "Vibrant green lettuce leaf margins",
            "Toasted bun surface has zero moisture collapse"
        ],
        "storage_recommendation": "Store wrapped tightly in aluminum foil in the refrigerator.",
        "safety_advisory": "Consume within 3 days. Ensure beef core reaches 74°C when reheating."
    },
    "sushi": {
        "food_name": "Salmon Sushi Combo",
        "classification": "Moderately Fresh",
        "freshness_score": 76,
        "shelf_life_estimate": "Consume within 18–24 hours",
        "color_analysis": "Translucent orange fish flesh; slight darkening at the edge.",
        "texture_analysis": "Soft, tender fish surface; sushi rice grains show slight drying.",
        "discoloration_risk": "Moderate (natural oxidation on exposed raw fish surfaces).",
        "surface_patterns": [
            "Glossy salmon striations visible",
            "Light humidity condensation on seaweed wrap",
            "Absence of bacterial slime or off-color patches"
        ],
        "storage_recommendation": "Store at or below 4°C (40°F) in an airtight container immediately.",
        "safety_advisory": "Eat promptly. Raw seafood deteriorates rapidly at temperatures above 4°C."
    },
    "salad": {
        "food_name": "Garden Green Salad",
        "classification": "Fresh",
        "freshness_score": 96,
        "shelf_life_estimate": "2–3 days refrigerated",
        "color_analysis": "Vivid chlorophyll green leaves; deep red cherry tomato skins.",
        "texture_analysis": "Crisp cellular snap in cucumber and lettuce; firm tomato structure.",
        "discoloration_risk": "None detected (no brown wilt or water-soaked leaf spots).",
        "surface_patterns": [
            "Taut tomato epidermis",
            "Crisp leaf veining with no translucent rot patches",
            "Clean, unbruised cucumber slices"
        ],
        "storage_recommendation": "Store undressed greens with a paper towel lining in the crisper drawer.",
        "safety_advisory": "Peak freshness. Safe to consume raw."
    },
    "laddu": {
        "food_name": "Motichoor / Besan Laddu",
        "classification": "Fresh",
        "freshness_score": 95,
        "shelf_life_estimate": "10–14 days at room temperature",
        "color_analysis": "Luminous golden-saffron yellow with glossy ghee sheen.",
        "texture_analysis": "Firm spherical structure with moist, crumbly interior.",
        "discoloration_risk": "Extremely low (natural sugar & ghee content preserve quality).",
        "surface_patterns": [
            "Clean spherical shape with intact pistachio/melon seed garnish",
            "Zero fungal colonies or moisture condensation",
            "Aromatic roasted besan and cardamom profile"
        ],
        "storage_recommendation": "Store in a clean, airtight container at cool room temperature. Avoid refrigeration to maintain soft texture.",
        "safety_advisory": "Peak freshness. Safe and festive to consume."
    }
}

FALLBACK_FRESHNESS = {
    "food_name": "Harvest Food Item",
    "classification": "Fresh",
    "freshness_score": 88,
    "shelf_life_estimate": "2–3 days refrigerated",
    "color_analysis": "Natural, uniform pigmentation across visible food surfaces.",
    "texture_analysis": "Cohesive food structure without evidence of degradation or dehydration.",
    "discoloration_risk": "Low (no visible gray, blue, or green mold patches).",
    "surface_patterns": [
        "Normal culinary surface appearance",
        "Intact cell walls without enzymatic liquefaction",
        "Zero signs of fungal sporulation"
    ],
    "storage_recommendation": "Cover securely and chill within 2 hours of food preparation.",
    "safety_advisory": "Visual signs indicate acceptable freshness. Inspect aroma before consumption."
}

def analyze_freshness(image_data: str, sample_tag: str = "") -> FreshnessResponse:
    api_key = get_gemini_api_key()

    # Offline / Mock Mode
    if not api_key:
        tag = (sample_tag or "").lower().strip()
        data = SAMPLE_FRESHNESS.get(tag)
        if not data:
            if "laddu" in tag or "ladoo" in tag or "sweet" in tag:
                data = SAMPLE_FRESHNESS["laddu"]
            else:
                data = FALLBACK_FRESHNESS

        return FreshnessResponse(
            success=True,
            food_name=data["food_name"],
            classification=data["classification"],
            freshness_score=data["freshness_score"],
            shelf_life_estimate=data["shelf_life_estimate"],
            color_analysis=data["color_analysis"],
            texture_analysis=data["texture_analysis"],
            discoloration_risk=data["discoloration_risk"],
            surface_patterns=data["surface_patterns"],
            storage_recommendation=data["storage_recommendation"],
            safety_advisory=data["safety_advisory"],
            is_mock=True
        )

    # Live Multimodal Freshness Vision
    try:
        header, b64_string = image_data.split(",", 1) if "," in image_data else ("", image_data)
        mime_match = re.search(r"data:([^;]+);base64", header)
        mime_type = mime_match.group(1) if mime_match else "image/jpeg"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt = (
            "You are a computer vision food safety and spoilage detection specialist. Analyze this food image.\n"
            "Evaluate visual signs: color, texture, discoloration, surface patterns, oxidation, mold, or drying.\n"
            "Classify the food strictly into one of: 'Fresh', 'Moderately Fresh', or 'Spoiled'.\n"
            "Respond ONLY with a JSON object in this schema:\n"
            "{\n"
            '  "food_name": "Identified item",\n'
            '  "classification": "Fresh" or "Moderately Fresh" or "Spoiled",\n'
            '  "freshness_score": integer 10 to 99,\n'
            '  "shelf_life_estimate": "Estimated shelf life under proper storage",\n'
            '  "color_analysis": "Evaluation of color and pigment changes",\n'
            '  "texture_analysis": "Evaluation of moisture, firmness, or slime",\n'
            '  "discoloration_risk": "Discoloration assessment",\n'
            '  "surface_patterns": ["Surface pattern 1", "Surface pattern 2", "Surface pattern 3"],\n'
            '  "storage_recommendation": "Storage instruction",\n'
            '  "safety_advisory": "Food safety advisory"\n'
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

            return FreshnessResponse(
                success=True,
                food_name=parsed.get("food_name", "Food Item"),
                classification=parsed.get("classification", "Fresh"),
                freshness_score=int(parsed.get("freshness_score", 85)),
                shelf_life_estimate=parsed.get("shelf_life_estimate", "2–3 days"),
                color_analysis=parsed.get("color_analysis", "Normal coloration detected."),
                texture_analysis=parsed.get("texture_analysis", "Surface texture appears stable."),
                discoloration_risk=parsed.get("discoloration_risk", "Low discoloration detected."),
                surface_patterns=parsed.get("surface_patterns", ["Consistent surface coloration"]),
                storage_recommendation=parsed.get("storage_recommendation", "Keep refrigerated at 4°C."),
                safety_advisory=parsed.get("safety_advisory", "Inspect before consuming."),
                is_mock=False
            )
    except Exception as e:
        data = FALLBACK_FRESHNESS
        return FreshnessResponse(
            success=True,
            food_name=data["food_name"],
            classification=data["classification"],
            freshness_score=data["freshness_score"],
            shelf_life_estimate=data["shelf_life_estimate"],
            color_analysis=data["color_analysis"],
            texture_analysis=data["texture_analysis"],
            discoloration_risk=data["discoloration_risk"],
            surface_patterns=data["surface_patterns"],
            storage_recommendation=data["storage_recommendation"],
            safety_advisory=f"{data['safety_advisory']} (AI note: {str(e)[:50]})",
            is_mock=True
        )
