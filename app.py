from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
from agent import generate_recommendations

app = Flask(__name__)
CORS(app)  # allow UI to call backend

# ---------------------------
# HEALTH CHECK
# ---------------------------
@app.route("/")
def health():
    return {"status": "Backend running"}

# ---------------------------
# GET ALL PATIENTS (UI TABLE)
# ---------------------------
@app.route("/api/patients", methods=["GET"])
def get_patients():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, gender, age, diagnosis, phone, address, blood_group, triage
        FROM patients
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    patients = []
    for r in rows:
        patients.append({
            "id": r[0],
            "name": r[1],
            "gender": r[2],
            "age": r[3],
            "diagnosis": r[4],
            "phone": r[5],
            "address": r[6],
            "blood": r[7],
            "triage": r[8],
            "avatar": "https://i.pravatar.cc/150"
        })

    return jsonify(patients)

# ---------------------------
# GET PATIENT + AI DECISION
# ---------------------------
@app.route("/api/patients/<int:patient_id>/decision", methods=["GET"])
def get_patient_decision(patient_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch patient vitals
    cur.execute("""
        SELECT avpu, sbp, spo2, rr, news2
        FROM patient_vitals
        WHERE patient_id = %s
        ORDER BY recorded_at DESC
        LIMIT 1
    """, (patient_id,))

    patient_row = cur.fetchone()

    # Fetch hospital resources
    cur.execute("""
        SELECT icu_beds_available, rrt_available, nurse_load, transport_delay
        FROM hospital_resources
        ORDER BY updated_at DESC
        LIMIT 1
    """)

    resource_row = cur.fetchone()
    cur.close()
    conn.close()

    if not patient_row or not resource_row:
        return jsonify({"error": "Missing data"}), 400

    patient = {
        "AVPU": patient_row[0],
        "SBP": patient_row[1],
        "SpO2": patient_row[2],
        "RR": patient_row[3],
        "NEWS2": patient_row[4],
    }

    resource_state = {
        "icu_beds_available": resource_row[0],
        "rrt_available": resource_row[1],
        "nurse_load": resource_row[2],
        "transport_delay": resource_row[3],
    }

    recommendations = generate_recommendations(patient, resource_state)

    return jsonify(recommendations)

# ---------------------------
# ADD PATIENT (OPTIONAL)
# ---------------------------
@app.route("/api/patients", methods=["POST"])
def add_patient():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (name, gender, age, diagnosis, phone, address, blood_group, triage)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id
    """, (
        data["name"], data["gender"], data["age"], data["diagnosis"],
        data["phone"], data["address"], data["blood"], data["triage"]
    ))

    patient_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": patient_id}), 201

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
