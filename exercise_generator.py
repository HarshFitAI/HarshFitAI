import json

exercises = []

muscle_groups = ["Chest", "Back", "Legs", "Core", "Shoulders", "Arms", "Full Body"]
goals = ["Fat Loss", "Strength", "Muscle Gain"]
difficulties = ["Beginner", "Intermediate", "Advanced"]
equipment_types = ["None", "Dumbbell", "Barbell"]

base_exercises = {
    "Chest": ["Push-ups", "Bench Press", "Chest Fly", "Incline Press"],
    "Back": ["Pull-ups", "Lat Pulldown", "Deadlift", "Seated Row"],
    "Legs": ["Squats", "Lunges", "Leg Press", "Romanian Deadlift"],
    "Core": ["Plank", "Crunches", "Russian Twists", "Leg Raises"],
    "Shoulders": ["Shoulder Press", "Lateral Raises", "Front Raises"],
    "Arms": ["Bicep Curl", "Tricep Dips", "Hammer Curl"],
    "Full Body": ["Burpees", "Mountain Climbers", "Jumping Jacks"]
}

for group in muscle_groups:
    for name in base_exercises.get(group, []):
        for goal in goals:
            for difficulty in difficulties:
                exercise = {
                    "name": f"{name} ({difficulty})",
                    "muscle_group": group,
                    "goal": goal,
                    "difficulty": difficulty,
                    "equipment": equipment_types[0],
                    "calories_per_10min": 60 if goal == "Fat Loss" else 40,
                    "sets": 3 if difficulty == "Beginner" else 4,
                    "reps": 12 if goal == "Muscle Gain" else 10,
                    "video_url": "https://www.youtube.com/results?search_query=" + name.replace(" ", "+")
                }
                exercises.append(exercise)

with open("database/exercises.json", "w") as f:
    json.dump(exercises, f, indent=4)

print("✅ Exercise database generated successfully!")