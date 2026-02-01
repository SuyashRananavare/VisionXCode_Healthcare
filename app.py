from flask import Flask, jsonify
from flask_cors import CORS

from agent.agent import generate_recommendations
from agent.documentation import get_action_documentation
from agent.explanation import explain_action_decision


from flask import render_template
app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# Serve the main page
@app.route("/")
def home():
    return render_template("index.html")

# --------------------------------------------------
# HOSPITAL STATE
# --------------------------------------------------

patients = [
    {
        "id": "P001",
        "name": "Patient 1",
        "AVPU": "A",
        "SBP": 110,
        "SpO2": 97,
        "RR": 18,
        "NEWS2": 2
    },
    {
        "id": "P002",
        "name": "Patient 2",
        "AVPU": "V",
        "SBP": 92,
        "SpO2": 91,
        "RR": 22,
        "NEWS2": 6
    },
    {
        "id": "P003",
        "name": "Patient 3",
        "AVPU": "A",
        "SBP": 88,
        "SpO2": 89,
        "RR": 24,
        "NEWS2": 7
    },
    {
        "id": "P004",
        "name": "Patient 4",
        "AVPU": "A",
        "SBP": 120,
        "SpO2": 99,
        "RR": 16,
        "NEWS2": 1
    },
    {
        "id": "P005",
        "name": "Patient 5",
        "AVPU": "P",
        "SBP": 85,
        "SpO2": 86,
        "RR": 28,
        "NEWS2": 9
    }
]

staff_state = {
    "nurses_total": 3,
    "nurse_load": 0.75,   # 75% busy
    "rrt_available": True
}

bed_state = {
    "icu_beds_available": 1,
    "ward_beds_available": 3
}

# --------------------------------------------------
# AGENT EXECUTION
# --------------------------------------------------

@app.route("/api/recommendations")
def recommendations():
    output = []

    for patient in patients:
        resource_state = {
            "icu_beds_available": bed_state["icu_beds_available"],
            "rrt_available": staff_state["rrt_available"],
            "nurse_load": staff_state["nurse_load"],
            "transport_delay": 20
        }

        recs = generate_recommendations(patient, resource_state)

        enriched = []
        for r in recs:
            doc = get_action_documentation(r["action"])
            explanation = explain_action_decision(r, [doc] if doc else [])

            enriched.append({
                **r,
                "documentation": doc[:300] + "..." if doc else "",
                "explanation": explanation
            })

        output.append({
            "patient_id": patient["id"],
            "name": patient["name"],
            "patient_state": patient,
            "recommendations": enriched
        })

    return jsonify({
        "hospital_state": {
            "beds": bed_state,
            "staff": staff_state
        },
        "patients": output
    })


# --------------------------------------------------
# SIMULATION: DETERIORATION + RESOURCE PRESSURE
# --------------------------------------------------

@app.route("/api/simulate")
def simulate():
    # Patient 2 deteriorates
    patients[1]["SpO2"] = 85
    patients[1]["NEWS2"] = 8

    # Patient 5 becomes critical
    patients[4]["SpO2"] = 82
    patients[4]["NEWS2"] = 10

    # ICU bed consumed
    bed_state["icu_beds_available"] = 0

    # Nurse overload
    staff_state["nurse_load"] = 0.92

    return jsonify({"status": "hospital state updated"})


if __name__ == "__main__":
    app.run(debug=True)
