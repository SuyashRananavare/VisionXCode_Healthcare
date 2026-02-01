"""
Demo script to visualize counterfactual reasoning.
Runs the agent on a scenario and prints recommendations with explanation.
"""
from dss_agent.agent import EscalationAgent
from dss_agent.models import Vitals, ResourceState

def run_demo():
    print("Initiating Counterfactual Demo...")
    agent = EscalationAgent("patient_001")
    
    # 1. Simulate a deteriorating patient (Sepsis-like)
    vitals = Vitals(
        avpu="A",
        sbp=95,  # Lowish
        spo2=92, # Lowish
        rr=24,   # High - Tachypnea
        hr=110,  # Tachycardia
        temp=38.5, # Fever
        news2=8   # High risk
    )
    
    resources = ResourceState(
        icu_beds_available=1,
        rrt_available=True,
        nurse_load=0.6,
        transport_delay_minutes=15
    )
    
    print("\nPatient State: deteriorating (NEWS2=8), Fever, Tachycardia, Tachypnea")
    
    # Run agent
    recommendations = agent.run_step(vitals, resources)
    
    print(f"\nRecommendations generated: {len(recommendations)}")
    
    for i, rec in enumerate(recommendations):
        print(f"\nRecommendation #{rec['rank']} (Confidence: {rec['confidence']:.2f}):")
        print(f"Action: {rec['action']}")
        print(f"Rationale: {rec['rationale']}")
        
        if rec.get('counterfactual_analysis'):
            cf = rec['counterfactual_analysis']
            print(f"\n[EXPLANATION] What if we wait 60 mins?")
            print(f"  Summary: {cf['summary']}")
            print(f"  Projected Risk: {cf['projected_risk']} (Change: {cf['risk_change']})")
            if cf['key_drivers']:
                print(f"  Key Drivers: {cf['key_drivers']}")
        else:
            print("  No counterfactual analysis available.")

if __name__ == "__main__":
    run_demo()
