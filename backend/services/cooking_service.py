"""
Food Verse AI - Smart Cooking Assistant Service
================================================
Multimodal cooking intelligence supporting:
- Speech / Voice prompt queries
- Text recipe search & ingredient inputs
- Computer vision ingredient photo identification
- Step-by-step guidance with timers and chef secrets
"""

import json
import urllib.request
import urllib.error
import re
from backend.config import get_gemini_api_key
from backend.models import CookingAssistantResponse, CookingStep

PRESET_RECIPES = {
    "pasta": {
        "recipe_name": "Garlic Butter Basil Pasta",
        "cuisine": "Italian",
        "prep_time": "10 mins",
        "cook_time": "15 mins",
        "difficulty": "Easy",
        "servings": 2,
        "ingredients": [
            "200g Fettuccine or Spaghetti pasta",
            "3 cloves garlic, thinly sliced",
            "2 tbsp extra-virgin olive oil",
            "2 tbsp unsalted butter",
            "1/2 cup fresh basil leaves, torn",
            "1/4 cup grated Parmigiano-Reggiano",
            "1/4 tsp red pepper flakes (optional)",
            "Sea salt and freshly cracked black pepper"
        ],
        "steps": [
            CookingStep(step_number=1, instruction="Bring a large pot of salted water to a rolling boil. Add pasta and cook until al dente.", timer_minutes=9, technique_tip="Reserve 1/2 cup of starchy pasta water before draining."),
            CookingStep(step_number=2, instruction="In a wide skillet over medium-low heat, warm olive oil and butter. Add sliced garlic and cook gently until fragrant and pale golden.", timer_minutes=3, technique_tip="Do not burn garlic; keep heat gentle."),
            CookingStep(step_number=3, instruction="Transfer drained hot pasta directly into the garlic skillet. Pour in 3 tablespoons of reserved pasta water and toss vigorously.", timer_minutes=2, technique_tip="Emulsification of starch and butter creates a glossy restaurant-quality sauce."),
            CookingStep(step_number=4, instruction="Remove from heat. Fold in torn fresh basil, grated parmesan, and cracked pepper. Serve immediately.", timer_minutes=1, technique_tip="Garnish with extra parmesan shavings.")
        ],
        "chef_secret": "Starchy pasta water is the magic secret that turns butter and olive oil into a silky, cohesive sauce that clings to every noodle.",
        "nutrition_per_serving": "Calories: 430 kcal | Protein: 12g | Carbs: 58g | Fat: 16g"
    },
    "stirfry": {
        "recipe_name": "Crispy Tofu & Rainbow Veggie Stir-Fry",
        "cuisine": "Asian Fusion",
        "prep_time": "15 mins",
        "cook_time": "12 mins",
        "difficulty": "Easy",
        "servings": 2,
        "ingredients": [
            "250g extra-firm tofu, pressed and cubed",
            "1 cup broccoli florets",
            "1 bell pepper, sliced into thin strips",
            "1 carrot, julienned",
            "2 tbsp tamari or low-sodium soy sauce",
            "1 tbsp sesame oil",
            "1 tsp cornstarch mixed with 2 tbsp water",
            "1 tsp grated fresh ginger and garlic"
        ],
        "steps": [
            CookingStep(step_number=1, instruction="Heat 1 tbsp oil in a wok or large skillet over high heat. Add tofu cubes and sear until golden and crisp on all sides.", timer_minutes=6, technique_tip="Press tofu with paper towels before frying to remove excess moisture."),
            CookingStep(step_number=2, instruction="Remove tofu. In the same hot pan, add ginger, garlic, and sliced vegetables. Stir-fry rapidly until crisp-tender.", timer_minutes=4, technique_tip="Keep veggies moving to preserve vivid color and crunch."),
            CookingStep(step_number=3, instruction="Pour in soy sauce, sesame oil, and cornstarch slurry. Stir until sauce thickens into a glossy glaze.", timer_minutes=2, technique_tip="The cornstarch thickens in 30-45 seconds."),
            CookingStep(step_number=4, instruction="Toss crispy tofu back into the glazed vegetables. Top with toasted sesame seeds and sliced scallions.", timer_minutes=1, technique_tip="Serve hot over jasmine rice or quinoa.")
        ],
        "chef_secret": "High heat and rapid tossing in a preheated wok creates authentic wok-hei aroma and prevents vegetables from becoming soggy.",
        "nutrition_per_serving": "Calories: 310 kcal | Protein: 19g | Carbs: 22g | Fat: 14g"
    }
}

DEFAULT_RECIPE = {
    "recipe_name": "Mediterranean Skillet Chicken & Herbs",
    "cuisine": "Mediterranean",
    "prep_time": "10 mins",
    "cook_time": "20 mins",
    "difficulty": "Easy",
    "servings": 2,
    "ingredients": [
        "2 boneless, skinless chicken breasts (approx. 350g)",
        "1 cup cherry tomatoes, halved",
        "1/2 cup Kalamata olives, pitted",
        "2 tbsp olive oil",
        "1 tsp dried oregano & thyme",
        "2 cloves minced garlic",
        "Juice of 1/2 fresh lemon",
        "Crumbled feta cheese and parsley for garnish"
    ],
    "steps": [
        CookingStep(step_number=1, instruction="Season chicken breasts generously with salt, pepper, dried oregano, and thyme on both sides.", timer_minutes=2, technique_tip="Pat chicken dry before seasoning for a better golden sear."),
        CookingStep(step_number=2, instruction="Heat 1 tbsp olive oil in a skillet over medium-high heat. Sear chicken breasts for 6-7 minutes per side until golden and internal temp reads 74°C (165°F). Transfer to a plate.", timer_minutes=14, technique_tip="Avoid moving chicken for the first 4 minutes to develop a savory crust."),
        CookingStep(step_number=3, instruction="In the same skillet, reduce heat to medium. Add minced garlic, cherry tomatoes, and olives. Sauté until tomatoes blister and release their sweet juices.", timer_minutes=4, technique_tip="Scrape up any golden browned bits from the pan bottom for flavor."),
        CookingStep(step_number=4, instruction="Return chicken to skillet, squeeze fresh lemon juice over everything, and simmer for 1 minute. Garnish with feta and fresh parsley.", timer_minutes=2, technique_tip="Rest chicken for 3 minutes before slicing to retain moisture.")
    ],
    "chef_secret": "Searing chicken in olive oil and simmering in the natural tomato juices infuses vibrant Mediterranean flavor with minimal effort.",
    "nutrition_per_serving": "Calories: 380 kcal | Protein: 38g | Carbs: 8g | Fat: 18g"
}

def generate_cooking_guidance(query_text: str = "", voice_transcript: str = "", ingredients_image: str = "", dietary_preference: str = "None") -> CookingAssistantResponse:
    api_key = get_gemini_api_key()
    user_prompt = voice_transcript or query_text or ""

    # Match presets in offline mode
    if not api_key:
        lower_prompt = user_prompt.lower()
        if "pasta" in lower_prompt or "noodle" in lower_prompt or "italian" in lower_prompt:
            data = PRESET_RECIPES["pasta"]
        elif "tofu" in lower_prompt or "stir" in lower_prompt or "veggie" in lower_prompt or "asian" in lower_prompt:
            data = PRESET_RECIPES["stirfry"]
        else:
            data = DEFAULT_RECIPE

        return CookingAssistantResponse(
            success=True,
            recipe_name=data["recipe_name"],
            cuisine=data["cuisine"],
            prep_time=data["prep_time"],
            cook_time=data["cook_time"],
            difficulty=data["difficulty"],
            servings=data["servings"],
            ingredients=data["ingredients"],
            steps=data["steps"],
            chef_secret=data["chef_secret"],
            nutrition_per_serving=data["nutrition_per_serving"]
        )

    # Live Multimodal AI Cooking Generation
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        parts = []

        system_instruction = (
            f"You are a master culinary chef and smart cooking assistant. "
            f"The user wants a personalized recipe. User input: '{user_prompt}'. "
            f"Dietary preference: '{dietary_preference}'.\n"
            "If an image is attached, detect the ingredients shown and incorporate them.\n"
            "Respond ONLY with a JSON object in this schema:\n"
            "{\n"
            '  "recipe_name": "Appealing recipe title",\n'
            '  "cuisine": "Cuisine style",\n'
            '  "prep_time": "Prep time (e.g. 15 mins)",\n'
            '  "cook_time": "Cook time (e.g. 20 mins)",\n'
            '  "difficulty": "Easy" or "Intermediate" or "Advanced",\n'
            '  "servings": 2,\n'
            '  "ingredients": ["Item 1 with measurement", "Item 2", "Item 3"],\n'
            '  "steps": [\n'
            '    {"step_number": 1, "instruction": "Clear step action", "timer_minutes": 5, "technique_tip": "Pro culinary tip"}\n'
            '  ],\n'
            '  "chef_secret": "One valuable culinary secret technique",\n'
            '  "nutrition_per_serving": "Calories: ~400 kcal | Protein: 25g | Carbs: 35g | Fat: 14g"\n'
            "}\n"
            "Do NOT include markdown formatting."
        )

        parts.append({"text": system_instruction})

        if ingredients_image and "," in ingredients_image:
            header, b64_string = ingredients_image.split(",", 1)
            mime_match = re.search(r"data:([^;]+);base64", header)
            mime_type = mime_match.group(1) if mime_match else "image/jpeg"
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": b64_string
                }
            })

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {"response_mime_type": "application/json"}
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
            text = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
            parsed = json.loads(text)

            steps_list = [CookingStep(**s) for s in parsed.get("steps", [])] or DEFAULT_RECIPE["steps"]

            return CookingAssistantResponse(
                success=True,
                recipe_name=parsed.get("recipe_name", "Chef's Creation"),
                cuisine=parsed.get("cuisine", "International"),
                prep_time=parsed.get("prep_time", "15 mins"),
                cook_time=parsed.get("cook_time", "20 mins"),
                difficulty=parsed.get("difficulty", "Easy"),
                servings=int(parsed.get("servings", 2)),
                ingredients=parsed.get("ingredients", ["Fresh ingredients"]),
                steps=steps_list,
                chef_secret=parsed.get("chef_secret", "Balance acidity with seasoning for rounded flavor."),
                nutrition_per_serving=parsed.get("nutrition_per_serving", "Calories: ~400 kcal")
            )
    except Exception as e:
        data = DEFAULT_RECIPE
        return CookingAssistantResponse(
            success=True,
            recipe_name=f"{data['recipe_name']} (Assistant Fallback)",
            cuisine=data["cuisine"],
            prep_time=data["prep_time"],
            cook_time=data["cook_time"],
            difficulty=data["difficulty"],
            servings=data["servings"],
            ingredients=data["ingredients"],
            steps=data["steps"],
            chef_secret=f"{data['chef_secret']} (AI Note: {str(e)[:45]})",
            nutrition_per_serving=data["nutrition_per_serving"]
        )
