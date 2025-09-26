from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Mock transport costs (realistic options)
def calculate_transport(origin, destination):
    options = []
    options.append({"mode": "Train", "cost": random.randint(300, 800)})
    options.append({"mode": "Bus", "cost": random.randint(200, 600)})
    # Only add flights if distance > 500 km (example)
    options.append({"mode": "Flight", "cost": random.randint(1500, 4000)} if abs(hash(destination) - hash(origin)) % 1000 > 500 else {"mode": "Flight", "cost": None})
    return options

@app.route("/generate", methods=["POST"])
def generate_itinerary():
    data = request.get_json()
    origin = data.get("origin")
    destination = data.get("destination")
    days = int(data.get("days"))
    interests = data.get("interests", [])

    # Transport
    transport_options = calculate_transport(origin, destination)
    cheapest_transport = min([t["cost"] for t in transport_options if t["cost"] is not None])

    # Daily plan
    morning_options = ["Sightseeing", "Museum", "Beach walk"]
    afternoon_options = ["Lunch at local cafe", "Shopping", "Park visit"]
    evening_options = ["Street food tour", "Nightlife", "Boat ride"]

    # Add interests
    if "Food" in interests:
        morning_options.append("Cooking class")
        evening_options.append("Food tasting")
    if "Beaches" in interests:
        morning_options.append("Beach games")
        afternoon_options.append("Beachside lunch")
    if "History" in interests:
        morning_options.append("Historical monument")
        afternoon_options.append("Heritage walk")
    if "Nature" in interests:
        morning_options.append("Nature hike")
        afternoon_options.append("Park visit")
    if "Museums" in interests:
        morning_options.append("Museum visit")
        afternoon_options.append("Art gallery")
    if "Nightlife" in interests:
        evening_options.append("Pub crawl")

    daily_plan = []
    for i in range(days):
        daily_plan.append({
            "day": i + 1,
            "morning": random.choice(morning_options),
            "afternoon": random.choice(afternoon_options),
            "evening": random.choice(evening_options),
            "cost": random.randint(400, 800)
        })

    total_cost = sum(d["cost"] for d in daily_plan) + cheapest_transport

    itinerary = {
        "summary": f"{days}-day trip from {origin} to {destination} with interests: {', '.join(interests)}",
        "transport": transport_options,
        "daily_plan": daily_plan,
        "total_cost": total_cost,
        "notes": "Stay in hostels or budget hotels. Meals at local eateries."
    }

    return jsonify({"itinerary": itinerary})

if __name__ == "__main__":
    app.run(debug=True)
