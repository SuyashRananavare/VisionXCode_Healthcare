from typing import List, Tuple
from ..models import PatientBeliefState, Vitals

def analyze_vital_trends(history: List[Vitals], current: Vitals) -> dict:
    """
    Analyzes trends in vital signs to detect deterioration or instability.
    Returns a dictionary of trend signals.
    """
    signals = {
        "stability": "stable",
        "trends": []
    }

    if not history:
        return signals

    # Simple slope check for key vitals (comparing last history point to current)
    last = history[-1]
    
    # Check for rapid drop in SBP
    if current.sbp < last.sbp - 20:
        signals["trends"].append("Rapid SBP drop")
        signals["stability"] = "unstable"
    
    # Check for rapid rise in RR
    if current.rr > last.rr + 5:
        signals["trends"].append("Rapid RR rise")
        signals["stability"] = "unstable"

    # Check for SpO2 drop
    if current.spo2 < last.spo2 - 5:
        signals["trends"].append("Significant SpO2 drop")
        signals["stability"] = "unstable"

    return signals
