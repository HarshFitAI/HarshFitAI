import streamlit as st
import json

st.set_page_config(page_title="HarshFit AI", page_icon="💪", layout="wide")

st.title("💪 HarshFit AI – Professional Fitness System")

# =============================
# LOAD DATABASES
# =============================

with open("database/exercises.json", "r") as f:
    exercises = json.load(f)

with open("database/meals.json", "r") as f:
    meals = json.load(f)

# =============================
# SIDEBAR SETTINGS
# =============================

st.sidebar.header("User Settings")

# Unique filter options
muscle_options = sorted(set(item["muscle_group"] for item in exercises))
goal_options = sorted(set(item["goal"] for item in exercises))
difficulty_options = sorted(set(item["difficulty"] for item in exercises))

muscle = st.sidebar.selectbox("Select Muscle Group", muscle_options)
goal = st.sidebar.selectbox("Select Goal", goal_options)
difficulty = st.sidebar.selectbox("Select Difficulty", difficulty_options)

height = st.sidebar.number_input("Your Height (cm)", 100, 250, 170)
weight = st.sidebar.number_input("Your Weight (kg)", 30, 200, 70)
age = st.sidebar.number_input("Your Age", 10, 100, 21)

calorie_target = st.sidebar.number_input(
    "Daily Calorie Target (kcal)", 1000, 5000, 2000
)

diet_type = st.sidebar.selectbox(
    "Diet Preference", ["Vegetarian", "Non-Vegetarian"]
)

# =============================
# BMI + WATER
# =============================

bmi = weight / ((height / 100) ** 2)

st.sidebar.markdown("### 📊 Your BMI")
st.sidebar.write(round(bmi, 2))

if bmi < 18.5:
    st.sidebar.info("Underweight")
elif 18.5 <= bmi < 25:
    st.sidebar.success("Normal Weight")
elif 25 <= bmi < 30:
    st.sidebar.warning("Overweight")
else:
    st.sidebar.error("Obese")

# Water recommendation
water_liters = round(weight * 0.035, 2)
st.sidebar.markdown("### 💧 Daily Water Intake")
st.sidebar.write(f"{water_liters} Liters per day")

# =============================
# GENERATE PLAN BUTTON
# =============================

if st.button("Generate Plan"):

    # =============================
    # EXERCISE SECTION
    # =============================

    st.subheader("🏋 Personalized Exercise Plan")

    filtered_exercises = [
        ex for ex in exercises
        if ex["muscle_group"] == muscle
        and ex["goal"] == goal
        and ex["difficulty"] == difficulty
    ]

    if filtered_exercises:
        total_calories = 0

        for ex in filtered_exercises:
            st.markdown(f"### {ex['name']}")
            st.write(f"Sets: {ex['sets']}")
            st.write(f"Reps: {ex['reps']}")
            st.write(f"Calories (10 min): {ex['calories_per_10min']} kcal")
            st.markdown(f"[🎥 Watch Video]({ex['video_url']})")
            st.markdown("---")

            total_calories += ex["calories_per_10min"]

        st.success(f"🔥 Estimated Calories Burn: {total_calories} kcal (10 min)")

    else:
        st.warning("No exercises found for selected filters.")

         # =============================
    # PROFESSIONAL MEAL PLAN
    # =============================

    st.subheader("🍽 Personalized Meal Plan")

    # Filter by diet
    filtered_meals = [
        meal for meal in meals
        if meal["type"] == diet_type
    ]

    if filtered_meals:

        breakfast_target = calorie_target * 0.3
        lunch_target = calorie_target * 0.4
        dinner_target = calorie_target * 0.3

        breakfast = [m for m in filtered_meals if m["meal_time"] == "Breakfast"]
        lunch = [m for m in filtered_meals if m["meal_time"] == "Lunch"]
        dinner = [m for m in filtered_meals if m["meal_time"] == "Dinner"]

        def display_meal(title, meal_list, target):
            st.markdown(f"### {title}")
            total = 0
            protein = 0
            carbs = 0
            fats = 0

            for m in meal_list:
                if total < target:
                    st.write(f"**{m['name']}**")
                    st.write(f"Calories: {m['calories']} kcal")
                    st.write(f"Protein: {m['protein']} g")
                    st.write(f"Carbs: {m['carbs']} g")
                    st.write(f"Fats: {m['fats']} g")
                    st.write(f"Quantity: {m['quantity']}")
                    st.markdown("---")

                    total += m["calories"]
                    protein += m["protein"]
                    carbs += m["carbs"]
                    fats += m["fats"]

            st.info(f"Target: {int(target)} kcal | Selected: {total} kcal")
            st.success(f"Protein: {protein}g | Carbs: {carbs}g | Fats: {fats}g")

        display_meal("🥣 Breakfast", breakfast, breakfast_target)
        display_meal("🍛 Lunch", lunch, lunch_target)
        display_meal("🍲 Dinner", dinner, dinner_target)

    else:
        st.warning("No meals found for selected diet.")