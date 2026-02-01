from datetime import datetime, timedelta
from ..models import PatientBeliefState

def check_delays(belief_state: PatientBeliefState) -> dict:
    """
    Checks for delays in review or treatment.
    """
    signals = {
        "overdue_review": False,
        "time_since_last_vitals_min": 0.0
    }
    
    current_time = datetime.now()
    if belief_state.current_vitals.timestamp:
        # Assuming timestamp is datetime object. If it's pure dataclass creation it might be now().
        # We need to ensure timestamps are managed correctly in simulation.
        # Here we calculate time delta.
        delta = current_time - belief_state.current_vitals.timestamp
        minutes_since = delta.total_seconds() / 60.0
        signals["time_since_last_vitals_min"] = round(minutes_since, 1)

        if minutes_since > 60: # Flag if vitals are older than 1 hour (just an example threshold)
            signals["overdue_review"] = True

    return signals
