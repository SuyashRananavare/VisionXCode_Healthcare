"""
Healthcare Agent Recommendation Module

This module provides a deterministic, auditable agent for generating clinical recommendations
based on patient vital signs and hospital resource state. It applies safety rules first,
then scores actions using risk and resource awareness.

Author: AI Assistant
Date: January 31, 2026
"""

from .observer import format_react_reasoning

from .documentation import get_action_documentation

from .explanation import explain_action_decision

def generate_recommendations(patient: dict, resource_state: dict) -> list[dict]:
    """
    Generate 1-3 ranked clinical recommendations for a patient.

    Args:
        patient (dict): Patient belief state containing vitals and NEWS2 score.
            Expected keys: 'AVPU', 'SBP', 'SpO2', 'RR', 'NEWS2', etc.
        resource_state (dict): Hospital resource state.
            Expected keys: 'icu_beds_available', 'rrt_available', 'nurse_load', 'transport_delay'

    Returns:
        list[dict]: List of 1-3 recommendation dictionaries, each containing:
            - action (str): Recommended action
            - rationale (str): 1-2 sentence explanation
            - expected_benefit (str): 'High', 'Medium', or 'Low'
            - cost (dict): {'level': 'High'|'Medium'|'Low', 'explanation': str}
            - confidence (float): 0.0-1.0
            - emergent (bool): True for immediate actions
    """
    # Extract patient data with defaults
    avpu = patient.get("AVPU", "A")
    sbp = patient.get("SBP", 120)
    spo2 = patient.get("SpO2", 98)
    rr = patient.get("RR", 16)
    news2 = patient.get("NEWS2", 0)

    # Extract resource data with defaults
    icu_beds = resource_state.get("icu_beds_available", 1)
    rrt_available = resource_state.get("rrt_available", True)
    nurse_load = resource_state.get("nurse_load", 0.5)
    transport_delay = resource_state.get("transport_delay", 0)  # minutes

    # Safety rules check - mandatory first
    emergent_recommendation = None
    if avpu != "A" or sbp < 70 or spo2 < 80 or rr > 35 or news2 >= 9:
        emergent_recommendation = {
            "action": "Call RRT",
            "rationale": f"Patient meets critical safety criteria: AVPU={avpu}, SBP={sbp}, SpO2={spo2}, RR={rr}, NEWS2={news2}. Immediate RRT response required.",
            "expected_benefit": "High",
            "cost": {
                "level": "Medium",
                "explanation": "RRT team mobilization and assessment",
            },
            "confidence": 0.95,
            "emergent": True,
        }

    # Calculate base risk from NEWS2 (normalized 0-1)
    base_risk = min(news2 / 20.0, 1.0)

    # Define possible actions with base properties
    possible_actions = [
        {
            "action": "Monitor closely",
            "base_score": 0.4,
            "benefit": "Low",
            "cost_level": "Low",
            "cost_exp": "Minimal resource use",
            "min_risk": 0.0,
        },
        {
            "action": "Increase monitoring frequency",
            "base_score": 0.6,
            "benefit": "Medium",
            "cost_level": "Low",
            "cost_exp": "Slight increase in nursing time",
            "min_risk": 0.1,
        },
        {
            "action": "Consult specialist",
            "base_score": 0.7,
            "benefit": "Medium",
            "cost_level": "Medium",
            "cost_exp": "Specialist time and coordination",
            "min_risk": 0.2,
        },
        {
            "action": "ICU transfer",
            "base_score": 0.9,
            "benefit": "High",
            "cost_level": "High",
            "cost_exp": "ICU bed and transport resources",
            "min_risk": 0.3,
        },
        {
            "action": "Prepare transfer plan / bed request",
            "base_score": 0.8,
            "benefit": "Medium",
            "cost_level": "Medium",
            "cost_exp": "Administrative coordination for bed request",
            "min_risk": 0.3,
        },
        {
            "action": "Discharge planning",
            "base_score": 0.2,
            "benefit": "Low",
            "cost_level": "Low",
            "cost_exp": "Planning time",
            "min_risk": 0.0,
        },
    ]

    # Score and filter actions
    scored_actions = []
    for action in possible_actions:
        # Skip actions below minimum risk threshold
        if base_risk < action["min_risk"]:
            continue

        # Skip ICU transfer if no beds available
        if action["action"] == "ICU transfer" and icu_beds == 0:
            continue

        # Only include transfer plan if ICU transfer not possible and risk warrants
        if action["action"] == "Prepare transfer plan / bed request":
            if icu_beds > 0 or base_risk < 0.3:
                continue

        score = action["base_score"] + base_risk * 0.4  # Risk adjustment

        # Resource-based adjustments
        if (
            action["cost_level"] == "High"
            and nurse_load > 0.9
            and emergent_recommendation is None
        ):
            score -= 0.3  # Penalize high-cost actions under high nurse load

        if action["action"] == "ICU transfer":
            score -= transport_delay / 60.0 * 0.1  # Penalty for transport delay

        # Ensure score doesn't go below 0
        score = max(score, 0.0)

        # Calculate confidence based on score and risk alignment
        confidence = round(min(max(score, 0.3), 1.0), 2)

        # Build rationale
        risk_level = (
            "low" if base_risk < 0.3 else "moderate" if base_risk < 0.6 else "high"
        )
        rationale = f"Patient NEWS2 score of {news2} indicates {risk_level} risk. "

        if action["action"] == "ICU transfer":
            rationale += f"ICU beds available: {icu_beds}. Transport delay: {transport_delay} minutes."
        elif action["action"] == "Prepare transfer plan / bed request":
            rationale += f"No ICU beds available (beds: {icu_beds}). Initiating transfer coordination."
        elif action["action"] == "Consult specialist":
            rationale += (
                "Specialist consultation recommended for elevated risk factors."
            )
        elif action["action"] == "Increase monitoring frequency":
            rationale += "Increased monitoring to track vital sign trends."
        elif action["action"] == "Monitor closely":
            rationale += "Standard monitoring appropriate for current risk level."
        elif action["action"] == "Discharge planning":
            rationale += "Patient stable, initiate discharge planning."

        recommendation = {
            "action": action["action"],
            "rationale": rationale,
            "expected_benefit": action["benefit"],
            "cost": {"level": action["cost_level"], "explanation": action["cost_exp"]},
            "confidence": round(confidence, 2),
            "emergent": False,
        }

        scored_actions.append((score, recommendation))

    # Sort by score descending
    scored_actions.sort(key=lambda x: x[0], reverse=True)

    # Extract recommendations
    recommendations = [rec for _, rec in scored_actions[:3]]

    # Prepend emergent recommendation if present
    if emergent_recommendation:
        recommendations.insert(0, emergent_recommendation)
        recommendations = recommendations[:3]  # Ensure max 3

    return recommendations



