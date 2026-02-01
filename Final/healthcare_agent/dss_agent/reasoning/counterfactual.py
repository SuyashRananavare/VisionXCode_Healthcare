"""
Counterfactual reasoning module for clinical decision support.
Estimates the potential risk increase if recommended actions are delayed.
"""
from typing import List, Dict, Any

def analyze_counterfactual(
    current_risk: float,
    delay_minutes: int,
    active_signals: List[str]
) -> Dict[str, Any]:
    """
    Estimates projected risk increase over time if action is delayed.
    
    Args:
        current_risk: Current risk score (0.0 to 1.0).
        delay_minutes: Hypothetical delay in minutes.
        active_signals: List of active signal names (e.g. from trends or alerts).
        
    Returns:
        Dict containing projected risk, change, drivers, and summary.
    """
    
    # Base configuration: linear risk drift per minute
    # A base rate of 0.001 means 60 mins = 0.06 risk increase (6%)
    BASE_RISK_PER_MINUTE = 0.001  
    
    # Multipliers for specific high-risk signals
    # These effectively start the "clock" faster
    SIGNAL_MULTIPLIERS = {
        "rapid_deterioration": 3.0,
        "sepsis_alert": 2.0,
        "emergent_safety_trigger": 5.0,
        "unstable_trend": 1.5,
        "hypoxia": 2.0,
        "hypotension": 2.5,
        "Rapid SBP drop": 2.5,
        "Rapid RR rise": 2.0,
        "Significant SpO2 drop": 2.0,
        "overdue_review": 1.5
    }
    
    # Calculate effective deterioration rate
    multiplier = 1.0
    key_drivers = []
    
    # Identify the highest impact driver
    for signal in active_signals:
        if signal in SIGNAL_MULTIPLIERS:
            if SIGNAL_MULTIPLIERS[signal] > multiplier:
                multiplier = SIGNAL_MULTIPLIERS[signal]
            key_drivers.append(signal)

    # Filter key_drivers to only those that actually increased the multiplier
    # Or just list all significant ones? Listing all active high-risk signals is better for explanation.
    # Let's keep all active signals that are in our dictionary as drivers.
    
    effective_rate = BASE_RISK_PER_MINUTE * multiplier
    
    # Calculate projected risk
    risk_increase = effective_rate * delay_minutes
    projected_risk = current_risk + risk_increase
    
    # Cap at 1.0
    projected_risk = min(1.0, projected_risk)
    
    # Recalculate actual change after cap
    actual_change = projected_risk - current_risk
    
    # Generate summary string
    summary = f"Delay of {delay_minutes} min projected to increase risk by {actual_change:.2f}."
    if key_drivers:
        summary += f" Driven by: {', '.join(key_drivers)}."
    else:
        summary += " Due to baseline physiologic drift."
        
    if projected_risk >= 1.0:
        summary += " Warning: Risk reaches critical saturation."

    return {
        "projected_risk": round(projected_risk, 3),
        "risk_change": round(actual_change, 3),
        "key_drivers": key_drivers,
        "summary": summary
    }
