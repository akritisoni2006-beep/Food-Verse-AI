"""
Food Verse AI - Personalized Meal Planning Service
==================================================
Computes Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE),
and generates adaptive, goal-oriented daily meal plans.
"""

from typing import List, Optional
from backend.models import MealPlanResponse, MealItem

def calculate_tdee(weight_kg: float, height_cm: float, age: int, activity_level: str) -> int:
    """Mifflin-St Jeor BMR equation with activity multiplier."""
    bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }
    multiplier = multipliers.get(activity_level, 1.4)
    return int(bmr * multiplier)

def generate_meal_plan(
    age: int = 28,
    weight_kg: float = 70.0,
    height_cm: float = 175.0,
    activity_level: str = "Moderately Active",
    dietary_goal: str = "Weight Loss",
    dietary_restrictions: Optional[List[str]] = None,
    target_calories: Optional[int] = None
) -> MealPlanResponse:
    restrictions = dietary_restrictions or []
    base_tdee = calculate_tdee(weight_kg, height_cm, age, activity_level)

    # Adjust calorie target based on goal
    if target_calories and target_calories > 800:
        daily_cals = target_calories
    else:
        if dietary_goal == "Weight Loss":
            daily_cals = max(1300, base_tdee - 450)
        elif dietary_goal == "Muscle Gain":
            daily_cals = base_tdee + 350
        elif dietary_goal == "Keto":
            daily_cals = max(1400, base_tdee - 250)
        elif dietary_goal == "High Protein":
            daily_cals = base_tdee
        elif dietary_goal == "Diabetic-Friendly":
            daily_cals = max(1400, base_tdee - 200)
        else:
            daily_cals = base_tdee

    # Macro distribution
    if dietary_goal == "Keto":
        macros = {"Carbs": "5% (20-30g)", "Protein": "25% (110g)", "Healthy Fats": "70% (130g)"}
        meals = [
            MealItem(meal_type="Breakfast", dish_name="Avocado & Spinach Omelet with Goat Cheese", calories=int(daily_cals * 0.28), macros="P: 22g | C: 4g | F: 32g", benefits="Ketogenic fuel with essential micronutrients and lutein.", prep_time="10 mins"),
            MealItem(meal_type="Lunch", dish_name="Wild Salmon Salad with Olive Oil & Walnuts", calories=int(daily_cals * 0.35), macros="P: 34g | C: 6g | F: 38g", benefits="High anti-inflammatory Omega-3 fatty acids.", prep_time="15 mins"),
            MealItem(meal_type="Dinner", dish_name="Garlic Butter Ribeye with Roasted Asparagus", calories=int(daily_cals * 0.27), macros="P: 38g | C: 5g | F: 30g", benefits="Satiating dinner providing bioavailable heme iron and zinc.", prep_time="20 mins"),
            MealItem(meal_type="Snack", dish_name="Roasted Almonds & Pumpkin Seeds with Sea Salt", calories=int(daily_cals * 0.10), macros="P: 8g | C: 3g | F: 14g", benefits="Magnesium-rich snack supporting muscle recovery.", prep_time="2 mins")
        ]
    elif dietary_goal == "Muscle Gain" or dietary_goal == "High Protein":
        macros = {"Protein": "35% (160g)", "Carbs": "45% (210g)", "Healthy Fats": "20% (45g)"}
        meals = [
            MealItem(meal_type="Breakfast", dish_name="Overnight Greek Yogurt Oats with Blueberries & Chia", calories=int(daily_cals * 0.25), macros="P: 32g | C: 55g | F: 9g", benefits="Slow-digesting complex carbs and probiotics.", prep_time="5 mins (prep ahead)"),
            MealItem(meal_type="Lunch", dish_name="Grilled Lemon Herb Chicken Bowl with Quinoa & Sweet Potato", calories=int(daily_cals * 0.35), macros="P: 45g | C: 65g | F: 12g", benefits="Optimal 3:1 carb-to-protein ratio for muscle hypertrophy.", prep_time="20 mins"),
            MealItem(meal_type="Dinner", dish_name="Seared Sirloin Steak with Steamed Broccoli & Jasmine Rice", calories=int(daily_cals * 0.30), macros="P: 48g | C: 52g | F: 14g", benefits="Creatine and branch-chain amino acids for recovery.", prep_time="25 mins"),
            MealItem(meal_type="Snack", dish_name="Whey / Plant Protein Smoothie with Peanut Butter & Banana", calories=int(daily_cals * 0.10), macros="P: 28g | C: 25g | F: 7g", benefits="Rapid muscle protein synthesis post-workout.", prep_time="5 mins")
        ]
    elif dietary_goal == "Diabetic-Friendly":
        macros = {"Complex Carbs": "35% (Low Glycemic)", "Protein": "30%", "Healthy Fats": "35%"}
        meals = [
            MealItem(meal_type="Breakfast", dish_name="Scrambled Eggs with Sautéed Kale, Tomatoes & Rye Toast", calories=int(daily_cals * 0.25), macros="P: 24g | C: 22g | F: 16g", benefits="High fiber and protein prevents morning blood glucose spikes.", prep_time="10 mins"),
            MealItem(meal_type="Lunch", dish_name="Mediterranean Lentil & Cucumber Salad with Feta", calories=int(daily_cals * 0.35), macros="P: 26g | C: 42g | F: 14g", benefits="Soluble fiber from lentils regulates insulin sensitivity.", prep_time="15 mins"),
            MealItem(meal_type="Dinner", dish_name="Baked Cod Fillet with Lemon Butter & Roasted Cauliflower", calories=int(daily_cals * 0.30), macros="P: 36g | C: 15g | F: 12g", benefits="Lean white fish with negligible glycemic load.", prep_time="20 mins"),
            MealItem(meal_type="Snack", dish_name="Sliced Apple with 1 Tbsp All-Natural Almond Butter", calories=int(daily_cals * 0.10), macros="P: 5g | C: 18g | F: 9g", benefits="Pectin fiber buffers carbohydrate digestion.", prep_time="3 mins")
        ]
    else:  # Weight Loss or Balanced
        macros = {"Protein": "30% (130g)", "Carbs": "40% (170g)", "Healthy Fats": "30% (55g)"}
        meals = [
            MealItem(meal_type="Breakfast", dish_name="Poached Egg Avocado Toast on Sprouted Grain Bread", calories=int(daily_cals * 0.25), macros="P: 18g | C: 32g | F: 14g", benefits="Rich in B-vitamins and monounsaturated oleic acid.", prep_time="8 mins"),
            MealItem(meal_type="Lunch", dish_name="Mediterranean Grilled Chicken Salad with Lemon Vinaigrette", calories=int(daily_cals * 0.35), macros="P: 38g | C: 26g | F: 15g", benefits="Satiating lean poultry paired with polyphenol-rich greens.", prep_time="15 mins"),
            MealItem(meal_type="Dinner", dish_name="Baked Herb Salmon with Roasted Asparagus & Wild Rice", calories=int(daily_cals * 0.30), macros="P: 35g | C: 34g | F: 16g", benefits="Cardioprotective EPA/DHA fatty acids and selenium.", prep_time="25 mins"),
            MealItem(meal_type="Snack", dish_name="Greek Yogurt with Mixed Berries & Walnuts", calories=int(daily_cals * 0.10), macros="P: 15g | C: 16g | F: 5g", benefits="Low-calorie antioxidant boost with active live cultures.", prep_time="3 mins")
        ]

    # Water recommendation: approx 35ml per kg body weight
    water_liters = round((weight_kg * 0.035), 1)

    coaching = [
        f"Daily caloric deficit/surplus calibrated for your {dietary_goal} objective.",
        f"Hydration target: Consume minimum {water_liters} Liters of water daily.",
        "Space meals 3.5 to 4.5 hours apart to sustain steady metabolic burn and energy."
    ]
    if restrictions:
        coaching.append(f"Excluded allergens / preferences: {', '.join(restrictions)}.")

    return MealPlanResponse(
        success=True,
        daily_calorie_target=daily_cals,
        macro_distribution=macros,
        plan_title=f"Personalized {dietary_goal} Nutrition Protocol",
        dietary_goal=dietary_goal,
        meals=meals,
        hydration_target=f"{water_liters} L / day",
        coaching_tips=coaching
    )
