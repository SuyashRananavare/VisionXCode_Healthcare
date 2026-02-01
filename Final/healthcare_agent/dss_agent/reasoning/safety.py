from typing import Optional
from ..models import PatientBeliefState, Recommendation, Cost

def check_safety_rules(belief_state: PatientBeliefState) -> Optional[Recommendation]:
    """
    Checks mandatory safety rules that override all other reasoning.
    Returns an emergent Recommendation if a rule is triggered, else None.
    """
    vitals = belief_state.current_vitals
    
    triggers = []
    if vitals.avpu != "A":
        triggers.append(f"AVPU={vitals.avpu}")
    if vitals.sbp < 70:
        triggers.append(f"SBP={vitals.sbp}")
    if vitals.spo2 < 80:
        triggers.append(f"SpO2={vitals.spo2}")
    if vitals.rr > 35:
        triggers.append(f"RR={vitals.rr}")
    if vitals.news2 >= 9:
        triggers.append(f"NEWS2={vitals.news2}")
        
    if triggers:
        return Recommendation(
            action="Call RRT",
            rationale=f"Patient meets critical safety criteria: {', '.join(triggers)}. Immediate RRT response required.",
            expected_benefit="High",
            cost=Cost(level="Medium", explanation="RRT team mobilization"),
            confidence=0.95,
            emergent=True,
            rank=1
        )
        
    return None
