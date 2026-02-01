from ..models import PatientBeliefState

def check_treatment_response(belief_state: PatientBeliefState) -> dict:
    """
    Checks if the patient is responding to active interventions.
    """
    signals = {
        "response_status": "unknown"
    }
    
    # Example logic: if "fluid_bolus" in active_interventions and SBP improved, response is positive.
    # This is a stub for more complex logic.
    
    if "fluid_bolus" in belief_state.active_interventions:
        # Check history to see if SBP went up
        if belief_state.history:
            prev_sbp = belief_state.history[-1].sbp
            curr_sbp = belief_state.current_vitals.sbp
            if curr_sbp > prev_sbp + 5:
                 signals["response_status"] = "responsive"
            elif curr_sbp < prev_sbp:
                 signals["response_status"] = "non_responsive"
            else:
                 signals["response_status"] = "no_significant_change"
    
    return signals
