from datetime import datetime, timedelta
from dss_agent.agent import EscalationAgent
from dss_agent.models import Vitals, ResourceState

def run_scenario():
    print("Initializing Escalation Agent...")
    agent = EscalationAgent(patient_id="P12345")
    
    # Define a scenario: Patient stable -> Deteriorating -> Critical
    scenario_steps = [
        {
            "desc": "Step 1: Baseline - Stable",
            "vitals": Vitals(avpu="A", sbp=120, spo2=98, rr=16, news2=0, timestamp=datetime.now()),
            "resources": ResourceState(icu_beds_available=2, rrt_available=True, nurse_load=0.5, transport_delay_minutes=15)
        },
        {
            "desc": "Step 2: Mild Deterioration",
            "vitals": Vitals(avpu="A", sbp=110, spo2=94, rr=21, news2=4, timestamp=datetime.now() + timedelta(hours=1)),
            "resources": ResourceState(icu_beds_available=2, rrt_available=True, nurse_load=0.6, transport_delay_minutes=15)
        },
        {
            "desc": "Step 3: Significant Deterioration (High Risk)",
            "vitals": Vitals(avpu="V", sbp=95, spo2=88, rr=26, news2=10, timestamp=datetime.now() + timedelta(hours=2)),
            "resources": ResourceState(icu_beds_available=1, rrt_available=True, nurse_load=0.8, transport_delay_minutes=20)
        },
        {
             "desc": "Step 4: Critical (Safety Trigger)",
             "vitals": Vitals(avpu="U", sbp=60, spo2=85, rr=10, news2=15, timestamp=datetime.now() + timedelta(hours=3)),
             "resources": ResourceState(icu_beds_available=0, rrt_available=True, nurse_load=0.9, transport_delay_minutes=30)
        }
    ]
    
    for step in scenario_steps:
        print(f"\n--- {step['desc']} ---")
        recs = agent.run_step(step["vitals"], step["resources"])
        
        for i, rec in enumerate(recs, 1):
            print(f"Rec #{i}: {rec['action']}")
            print(f"   Rationale: {rec['rationale']}")
            print(f"   Confidence: {rec['confidence']}")
            print(f"   Emergent: {rec['emergent']}")

if __name__ == "__main__":
    run_scenario()
