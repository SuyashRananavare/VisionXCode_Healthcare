"""
Demo script to visualize explicit monitoring intent and memory narrative.
Shows how the agent decides to MONITOR and remembers history.
"""
from dss_agent.agent import EscalationAgent
from dss_agent.models import Vitals, ResourceState
from datetime import datetime, timedelta

def run_demo():
    agent = EscalationAgent("patient_monitor_demo")
    
    # Initial State: Stable
    vitals_t0 = Vitals(
        timestamp=datetime.now() - timedelta(hours=1),
        avpu="A", sbp=120, spo2=98, rr=16, news2=1
    )
    resources = ResourceState(icu_beds_available=1, rrt_available=True, nurse_load=0.5, transport_delay_minutes=10)
    
    print("\n--- T=0: Initial Assessment ---")
    recs_t0 = agent.run_step(vitals_t0, resources)
    print_decision(recs_t0)
    
    # T=1: Deterioration (RR increases, SpO2 drops)
    vitals_t1 = Vitals(
        timestamp=datetime.now(),
        avpu="A", sbp=115, spo2=94, rr=24, news2=5
    )
    
    print("\n--- T=1: Assessment (1 hr later) ---")
    recs_t1 = agent.run_step(vitals_t1, resources)
    print_decision(recs_t1)
    
    
def print_decision(recommendations):
    primary_rec = recommendations[0]
    
    if primary_rec['intent'] == "monitor":
        print(f"Agent decision: continue monitoring. No escalation yet.")
        print(f"Reason: {primary_rec['rationale']}")
        print(f"Next check-in: {primary_rec['next_check_in_minutes']} minutes")
    elif primary_rec['intent'] == "escalate":
        print(f"Agent decision: ESCALATION RECOMMENDED.")
        print(f"Action: {primary_rec['action']}")
        print(f"Reason: {primary_rec['rationale']}")
        
    if primary_rec.get('memory_narrative'):
        print("\nSince the last assessment:")
        for line in primary_rec['memory_narrative']:
            print(f"- {line}")

if __name__ == "__main__":
    run_demo()
