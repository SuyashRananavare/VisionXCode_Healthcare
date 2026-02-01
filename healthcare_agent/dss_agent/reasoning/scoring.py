from typing import List
from ..models import PatientBeliefState, ResourceState, Recommendation, Cost

def score_actions(belief_state: PatientBeliefState, resource_state: ResourceState, possible_actions: List[dict]) -> List[Recommendation]:
    """
    Scores and ranks possible actions based on risk, resources, and policy.
    """
    vitals = belief_state.current_vitals
    # Normalized risk 0-1
    base_risk = min(vitals.news2 / 20.0, 1.0)
    
    scored_recs = []
    
    for action_def in possible_actions:
        # 1. Filter by minimum risk
        if base_risk < action_def.get("min_risk", 0.0):
            continue
            
        # 2. Hard resource checks
        if action_def["action"] == "ICU transfer" and resource_state.icu_beds_available == 0:
            continue
            
        # 3. Conditional logic for specific actions
        if action_def["action"] == "Prepare transfer plan / bed request":
            # Only if ICU is full OR risk is high enough to warrant pre-planning but not immediate transfer?
            # Original logic: if icu_beds > 0 or base_risk < 0.3: continue
            if resource_state.icu_beds_available > 0 and base_risk < 0.6: # Relaxed slightly for this implementation
                 continue

        # 4. Calculate Score
        score = action_def["base_score"] + base_risk * 0.4
        
        # Resource penalties
        if action_def["cost_level"] == "High" and resource_state.nurse_load > 0.9:
            score -= 0.3
            
        if action_def["action"] == "ICU transfer":
            # Penalty for transport delay (e.g., 0.1 per hour)
            score -= (resource_state.transport_delay_minutes / 60.0) * 0.1
            
        score = max(score, 0.0)
        
        # 5. Confidence calibration
        # Confidence increases with score and risk
        confidence = min(max(score, 0.3), 1.0)
        
        # 6. Rationale generation
        rationale = _generate_rationale(action_def, belief_state, resource_state, base_risk)
        
        rec = Recommendation(
            action=action_def["action"],
            rationale=rationale,
            expected_benefit=action_def["benefit"],
            cost=Cost(level=action_def["cost_level"], explanation=action_def["cost_exp"]),
            confidence=round(confidence, 2),
            emergent=False
        )
        scored_recs.append((score, rec))
        
    # Sort and rank
    scored_recs.sort(key=lambda x: x[0], reverse=True)
    
    final_recs = []
    for rank, (score, rec) in enumerate(scored_recs, 1):
        rec.rank = rank
        final_recs.append(rec)
        
    return final_recs

def _generate_rationale(action_def, belief_state, resource_state, base_risk):
    risk_desc = "high" if base_risk > 0.6 else "moderate" if base_risk > 0.3 else "low"
    base = f"Patient has {risk_desc} risk (NEWS2={belief_state.current_vitals.news2})."
    
    if action_def["action"] == "ICU transfer":
        return f"{base} ICU beds: {resource_state.icu_beds_available}. Delay: {resource_state.transport_delay_minutes}m."
    elif action_def["action"] == "Prepare transfer plan / bed request":
        return f"{base} ICU full (0 beds). Initiating contingency planning."
    
    return base + " " + action_def.get("rationale_template", "Action appropriate for risk level.")
