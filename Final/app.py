from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sys
import os

# Ensure system path includes current directory for module lookups
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Backend Imports
from healthcare_agent.dss_agent.agent import EscalationAgent
from healthcare_agent.dss_agent.models import Vitals, ResourceState
from healthcare_agent.dss_agent.explainability.athena_stub import fetch_athena_guidelines
from healthcare_agent.dss_agent.explainability.llm_stub import generate_explanation

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# --------------------------------------------------
# UTILS
# --------------------------------------------------

def get_action_documentation(action_name):
    return fetch_athena_guidelines(action_name)

def explain_action_decision(recommendation, docs):
    context = {
        "recommendation": recommendation,
        "docs": docs
    }
    return generate_explanation(context)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

# Serve the "Integrated One" frontend - The Agent Interface
@app.route("/")
def agent_ui():
    return render_template("agent.html")

@app.route("/api/agent/run", methods=["POST"])
def run_agent_interactive():
    try:
        data = request.json
        vitals_data = data.get("vitals", {})
        resource_data = data.get("resources", {})
        
        # 1. Create Models
        vitals = Vitals(
            avpu=vitals_data.get("avpu", "A"),
            sbp=int(vitals_data.get("sbp", 120)),
            spo2=int(vitals_data.get("spo2", 98)),
            rr=int(vitals_data.get("rr", 18)),
            hr=80,  # Default
            temp=37.0,
            news2=int(vitals_data.get("news2", 0))
        )
        
        r_state = ResourceState(
            icu_beds_available=int(resource_data.get("icu_beds_available", 0)),
            rrt_available=resource_data.get("rrt_available", True),
            nurse_load=float(resource_data.get("nurse_load", 0.5)),
            transport_delay_minutes=20
        )
        
        # 2. Run Agent
        # Use a temporary ID since this is stateless per request for the demo
        temp_id = "SESSION_INTERACTIVE" 
        agent = EscalationAgent(patient_id=temp_id)
        
        recs = agent.run_step(vitals, r_state)
        
        # 3. Enrich Recommendations with Docs & Explanations
        enriched = []
        for r in recs:
            doc = get_action_documentation(r["action"])
            explanation = explain_action_decision(r, [doc] if doc else [])
            
            enriched.append({
                **r,
                "documentation": doc,
                "explanation": explanation
            })
            
        return jsonify({
            "status": "success",
            "recommendations": enriched,
            "patient_risk_score": vitals.news2
        })
        
    except Exception as e:
        print(f"Error running agent: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    # Ensure templates exist
    if not os.path.exists("templates/agent.html"):
        print("CRITICAL: templates/agent.html not found. Please ensure file exists.")
    
    app.run(host="127.0.0.1", port=5000, debug=True)
