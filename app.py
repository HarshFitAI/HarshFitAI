import streamlit as st
import json

st.set_page_config(page_title="HarshFit AI", layout="wide")

# =========================
# LOAD DATABASE
# =========================
with open("database/exercises.json") as f:
    exercises = json.load(f)

with open("database/yoga.json") as f:
    yoga_data = json.load(f)

with open("database/meals.json") as f:
    meals = json.load(f)

# =========================
# SIDEBAR INPUTS
# =========================
st.sidebar.title("User Settings")

muscle = st.sidebar.selectbox("Select Muscle Group", list(exercises.keys()))
goal = st.sidebar.selectbox("Select Goal", ["Fat Loss", "Muscle Gain"])
difficulty = st.sidebar.selectbox("Select Difficulty", ["Beginner", "Intermediate", "Advanced"])
yoga_level = st.sidebar.selectbox("Yoga Difficulty", ["Beginner", "Intermediate", "Advanced"])
day = st.sidebar.selectbox("Workout Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

calorie_target = st.sidebar.number_input("Daily Calorie Target", value=2000)
diet_pref = st.sidebar.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian"])

height = st.sidebar.number_input("Your Height (cm)", min_value=120, max_value=220, value=170)
weight = st.sidebar.number_input("Your Weight (kg)", min_value=30, max_value=200, value=75)
age = st.sidebar.number_input("Your Age", min_value=10, max_value=80, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

# =========================
# BODY CALCULATIONS
# =========================

bmi = weight / ((height / 100) ** 2)

if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

maintenance_calories = bmr * 1.4
fat_loss_calories = maintenance_calories - 500
water_intake = weight * 0.035

# =========================
# MAIN PAGE
# =========================

st.title("💪 HarshFit AI – Professional Fitness System")

generate = st.button("Generate Plan")

if generate:

    # ===== BODY ANALYSIS =====
    st.markdown("## 📊 Body Analysis")
    st.write(f"**BMI:** {bmi:.2f}")

    if bmi < 18.5:
        st.write("Category: Underweight")
    elif bmi < 25:
        st.write("Category: Normal Weight")
    elif bmi < 30:
        st.write("Category: Overweight")
    else:
        st.write("Category: Obese")

    st.write(f"**Maintenance Calories:** {maintenance_calories:.0f} kcal")
    st.write(f"**Fat Loss Calories:** {fat_loss_calories:.0f} kcal")
    st.write(f"**Recommended Water Intake:** {water_intake:.2f} Liters/day")

    st.divider()

    # ===== EXERCISE PLAN =====
    st.subheader("🏋 Exercise Plan")

    for ex in exercises[muscle][difficulty]:
        st.markdown(f"""
        ### {ex['name']}
        - Sets: {ex['sets']}
        - Reps: {ex['reps']}
        - Rest: {ex['rest']}
        - Calories Burn (10 min): {ex['calories']}
        """)

    st.divider()

    # ===== YOGA PLAN =====
    st.subheader("🧘 Yoga Plan")

    yoga_found = False

    for y in yoga_data:
        if y["level"] == yoga_level:
            yoga_found = True
            st.markdown(f"""
            ### {y['name']}
            - Duration: {y['duration']}
            - Benefit: {y['benefit']}
            """)

    if not yoga_found:
        st.info("No yoga found for selected level.")

    st.divider()

    # ===== MEAL PLAN =====
    st.subheader("🥗 Daily Meal Plan")

    total = 0

    for meal in meals:
        if meal["type"] == diet_pref:
            st.markdown(f"""
            ### {meal['name']}
            - Quantity: {meal['quantity']}
            - Calories: {meal['calories']} kcal
            """)
            total += meal["calories"]

    st.write(f"### 🔥 Total Planned Calories: {total} kcal")
