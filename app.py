import streamlit as st
import json

st.set_page_config(page_title="HarshFit AI", layout="wide")

st.title("💪 HarshFit AI – Professional Fitness System")

# -------------------------
# Load Databases
# -------------------------
with open("database/exercises.json") as f:
    exercises = json.load(f)

with open("database/yoga.json") as f:
    yoga_data = json.load(f)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("User Settings")

muscle_group = st.sidebar.selectbox(
    "Select Muscle Group",
    ["Chest", "Back", "Legs", "Core", "Shoulders", "Arms", "Full Body"]
)

goal = st.sidebar.selectbox(
    "Select Goal",
    ["Fat Loss", "Strength", "Muscle Gain"]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

yoga_difficulty = st.sidebar.selectbox(
    "Yoga Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

week_day = st.sidebar.selectbox(
    "Workout Day",
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
)
calorie_target = st.sidebar.number_input(
    "Daily Calorie Target",
    min_value=1200,
    max_value=4000,
    value=2000,
    step=100
)

diet_type = st.sidebar.selectbox(
    "Diet Preference",
    ["Vegetarian", "Non-Vegetarian"]
)
height = st.sidebar.number_input(
    "Your Height (cm)",
    min_value=120,
    max_value=220,
    value=170
)

# -------------------------
# Generate Plan
# -------------------------
if st.button("Generate Plan"):

    st.subheader(f"📅 Workout Plan for {week_day}")

    # -------------------------
    # Exercise Section
    # -------------------------
    st.subheader("🏋️ Exercise Plan")

    filtered_exercises = [
        ex for ex in exercises
        if ex["muscle_group"] == muscle_group
        and ex["goal"] == goal
        and ex["difficulty"] == difficulty
    ]

    if filtered_exercises:

        for ex in filtered_exercises[:5]:

            if goal == "Fat Loss":
                sets = 3
                reps = "15-20"
                rest = "30 sec"
            elif goal == "Strength":
                sets = 5
                reps = "5-8"
                rest = "90 sec"
            else:
                sets = 4
                reps = "8-12"
                rest = "60 sec"

            st.markdown(f"""
### 🏋 {ex['name']}
🎯 Goal: {goal}  
💪 Muscle: {muscle_group}  
🔥 Calories (10 min): {ex['calories_per_10min']}  
📊 Sets: {sets} | Reps: {reps} | Rest: {rest}  
▶ [Watch Demo]({ex['video_url']})
""")
            st.divider()
    else:
        st.warning("No exercises found.")

    # -------------------------
    # Smart Yoga Section
    # -------------------------
    st.subheader("🧘 Yoga Plan")

    # Step 1: Try exact match
    yoga_filtered = [
        y for y in yoga_data
        if y["focus"] == muscle_group
        and y["difficulty"] == yoga_difficulty
    ]

    # Step 2: Smart fallback if empty
    if not yoga_filtered:

        fallback_levels = {
            "Advanced": ["Intermediate", "Beginner"],
            "Intermediate": ["Beginner"],
            "Beginner": []
        }

        for level in fallback_levels[yoga_difficulty]:
            yoga_filtered = [
                y for y in yoga_data
                if y["focus"] == muscle_group
                and y["difficulty"] == level
            ]
            if yoga_filtered:
                st.info(f"⚠ Advanced not available. Showing {level} level yoga instead.")
                break

    # Step 3: Display yoga
    if yoga_filtered:
        for y in yoga_filtered[:3]:
            st.markdown(f"""
### 🧘 {y['name']}
💪 Focus: {y['focus']}
⚡ Difficulty: {y['difficulty']}
⏱ Duration: {y['duration']}
🌿 Benefits: {y['benefits']}
▶ [Watch Demo]({y['video_url']})
""")
            st.divider()
    else:
        st.warning("No yoga available for this muscle group.")
    # -------------------------
    # Meal Plan Section
    # -------------------------
    st.subheader("🥗 Daily Meal Plan")

    with open("database/meals.json") as f:
        meals = json.load(f)

    filtered_meals = [
        m for m in meals
        if m["type"] == diet_type
    ]

    total_calories = 0
    selected_meals = []

    for meal in filtered_meals:
        if total_calories + meal["calories"] <= calorie_target:
            selected_meals.append(meal)
            total_calories += meal["calories"]

    if selected_meals:
        for m in selected_meals:
            st.markdown(f"""
### 🍽 {m['name']}
📦 Quantity: {m['quantity']}
🔥 Calories: {m['calories']}
🥩 Protein: {m['protein']}g
🍞 Carbs: {m['carbs']}g
🥑 Fats: {m['fats']}g
""")
            st.divider()

        st.success(f"Total Calories: {total_calories} / {calorie_target}")
    else:
        st.warning("No meal combination found for selected calories.")
    # -------------------------
    # Water Intake
    # -------------------------
    st.subheader("💧 Daily Water Recommendation")

    body_weight = st.sidebar.number_input(
        "Your Weight (kg)",
        min_value=40,
        max_value=200,
        value=70
    )

    water_liters = round(body_weight * 0.035, 2)

    st.info(f"Recommended Water Intake: {water_liters} Liters per day")
        # -------------------------
    # Macro Calculation
    # -------------------------
    st.subheader("📊 Macro Distribution")

    if goal == "Fat Loss":
        protein_ratio = 0.40
        carb_ratio = 0.35
        fat_ratio = 0.25
    elif goal == "Muscle Gain":
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
    else:  # Strength
        protein_ratio = 0.35
        carb_ratio = 0.40
        fat_ratio = 0.25

    protein_cal = calorie_target * protein_ratio
    carb_cal = calorie_target * carb_ratio
    fat_cal = calorie_target * fat_ratio

    protein_grams = round(protein_cal / 4)
    carb_grams = round(carb_cal / 4)
    fat_grams = round(fat_cal / 9)

    st.write(f"🥩 Protein: {protein_grams}g")
    st.write(f"🍞 Carbs: {carb_grams}g")
    st.write(f"🥑 Fats: {fat_grams}g")
    # -------------------------
    # BMI Calculation
    # -------------------------
    st.subheader("🧮 Body Analysis")

    height_m = height / 100
    bmi = round(body_weight / (height_m ** 2), 2)

    st.write(f"BMI: {bmi}")

    if bmi < 18.5:
        st.info("Underweight")
    elif 18.5 <= bmi < 24.9:
        st.success("Normal Weight")
    elif 25 <= bmi < 29.9:
        st.warning("Overweight")
    else:
        st.error("Obese")

    # Rough Body Fat Estimate (AI Approximation)
    body_fat = round((1.20 * bmi) + (0.23 * 25) - 16.2, 2)
    st.write(f"Estimated Body Fat: {body_fat}%")
    # -------------------------
    # Progress Tracker
    # -------------------------
    st.subheader("📈 Weekly Progress")

    import os

    if os.path.exists("progress.json"):
        with open("progress.json") as f:
            progress = json.load(f)
    else:
        progress = []

    if st.button("Save Current Weight"):
        progress.append({"weight": body_weight})
        with open("progress.json", "w") as f:
            json.dump(progress, f)
        st.success("Progress Saved!")

    if progress:
        weights = [p["weight"] for p in progress]
        st.line_chart(weights)
    # -------------------------
    # Fat Loss Timeline
    # -------------------------
    st.subheader("⏳ Fat Loss Timeline")

    target_weight = st.number_input(
        "Target Weight (kg)",
        min_value=40,
        max_value=200,
        value=body_weight
    )

    if body_weight > target_weight:
        weight_to_lose = body_weight - target_weight
        weeks_needed = round(weight_to_lose / 0.5, 1)  # 0.5kg safe per week
        st.write(f"Estimated Time: {weeks_needed} weeks (Safe Fat Loss)")
    else:
        st.write("You are already at or below target weight.")
