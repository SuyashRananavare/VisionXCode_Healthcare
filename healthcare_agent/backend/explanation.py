"""
Clinical Explanation Assistant Module

This module provides clear, professional explanations for clinical action decisions,
focusing on patient risk factors and system constraints without suggesting alternatives
or modifying the final decision.

"""


def explain_action_decision(action: dict, evidence_snippets: list[str]) -> str:
    """
    Generate a simple, professional explanation for a clinical action decision.

    Args:
        action (dict): The action recommendation dictionary containing action details.
        evidence_snippets (list[str]): List of evidence snippets supporting the action.

    Returns:
        str: 2-3 short paragraphs explaining the decision in neutral clinical tone.
    """
    action_name = action.get("action", "")
    rationale = action.get("rationale", "")
    confidence = action.get("confidence", 0.0)
    emergent = action.get("emergent", False)

    # Extract key elements from rationale
    risk_factors = []
    constraints = []
    risk_level = "unknown"

    if "NEWS2 score" in rationale:
        # Extract NEWS2 score
        import re
        news_match = re.search(r'NEWS2 score of (\d+)', rationale)
        if news_match:
            news_score = int(news_match.group(1))
            risk_level = "low" if news_score < 3 else "moderate" if news_score < 7 else "high"
            risk_factors.append(f"NEWS2 score of {news_score} indicating {risk_level} risk")

    if "critical safety criteria" in rationale:
        risk_factors.append("meeting critical safety criteria requiring immediate response")

    if "ICU beds available" in rationale:
        beds_match = re.search(r'ICU beds available: (\d+)', rationale)
        if beds_match:
            beds = int(beds_match.group(1))
            if beds == 0:
                constraints.append("no ICU beds available")
            else:
                constraints.append(f"{beds} ICU beds available")

    if "Transport delay" in rationale:
        delay_match = re.search(r'Transport delay: (\d+) minutes', rationale)
        if delay_match:
            delay = int(delay_match.group(1))
            constraints.append(f"{delay} minute transport delay")

    # Build explanation
    explanation = []

    # Paragraph 1: Why this action
    para1 = f"This action was selected based on the patient's current clinical status. "
    if risk_factors:
        para1 += f"Key risk factors include {', '.join(risk_factors)}. "
    if emergent:
        para1 += "The situation requires immediate attention due to safety protocol triggers. "
    else:
        para1 += "The recommendation aligns with standard clinical guidelines for this risk level. "
    if evidence_snippets:
        para1 += "Supporting evidence from clinical guidelines confirms this approach is appropriate."
    explanation.append(para1)

    # Paragraph 2: How risk and constraints influenced
    para2 = "Patient risk assessment and system resource availability both played important roles in this decision. "
    if risk_factors:
        para2 += f"The identified risk factors necessitated a response that addresses the {risk_level} level of concern. "
    if constraints:
        para2 += f"System constraints, including {', '.join(constraints)}, were considered to ensure the action is feasible and timely. "
    else:
        para2 += "Available resources support implementation of this recommendation. "
    para2 += "This balanced approach prioritizes patient safety while respecting operational limitations."
    explanation.append(para2)

    # Optional paragraph 3: Evidence context
    if evidence_snippets and len(evidence_snippets) > 0:
        para3 = "Clinical evidence supports this decision through established protocols and best practices. "
        para3 += "The chosen action follows guidelines designed to optimize patient outcomes in similar situations."
        explanation.append(para3)


    return "\n\n".join(explanation)
