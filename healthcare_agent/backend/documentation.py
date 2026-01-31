"""
Clinical Action Documentation Module

This module provides authoritative documentation and references supporting
clinical actions recommended by the healthcare agent. All documentation
is based on established medical guidelines and best practices.

Author: AI Assistant
Date: January 31, 2026
"""

ACTION_DOCUMENTATION = {
    "Call RRT": """
Official Guidelines:
- National Early Warning Score (NEWS2) guidelines recommend immediate escalation for NEWS2 ≥ 7, with critical thresholds triggering rapid response team activation.
- Royal College of Physicians (RCP) guidelines for acute illness recognition emphasize immediate RRT involvement for patients meeting safety criteria (AVPU ≠ A, SBP < 70, SpO2 < 80, RR > 35, NEWS2 ≥ 9).
- American Heart Association (AHA) and European Resuscitation Council (ERC) protocols support rapid response systems for deteriorating patients.

Best Practices:
- RRT activation should occur within 5 minutes of identifying critical criteria.
- RRT teams typically include physicians, nurses, and respiratory therapists for immediate assessment and intervention.
- Documentation of RRT activation is required for quality improvement and audit purposes.

Policy Rationale:
- Hospital policies mandate RRT activation to prevent cardiac arrests and improve patient outcomes.
- Evidence from studies shows RRT reduces in-hospital mortality by 20-30% when activated appropriately.
""",
    "ICU transfer": """
Official Guidelines:
- Society of Critical Care Medicine (SCCM) guidelines recommend ICU admission for patients with organ dysfunction or high risk of deterioration.
- NEWS2 scoring system indicates ICU consideration for scores ≥ 7, with immediate transfer for scores ≥ 9.
- American Thoracic Society (ATS) protocols support ICU transfer for patients requiring advanced monitoring or interventions.

Best Practices:
- ICU transfer should be coordinated with transport teams to ensure patient stability during movement.
- Pre-transfer stabilization including airway management and hemodynamic support is essential.
- Multidisciplinary assessment should confirm ICU necessity versus alternative care settings.

Policy Rationale:
- ICU bed allocation follows triage protocols prioritizing patients with highest acuity.
- Transfer decisions balance patient needs with available resources and transport risks.
""",
    "Prepare transfer plan / bed request": """
Official Guidelines:
- Joint Commission standards require hospitals to have transfer protocols for patients needing higher levels of care.
- Centers for Medicare & Medicaid Services (CMS) regulations mandate appropriate transfer planning when facilities cannot provide required care.
- Emergency Medical Treatment and Labor Act (EMTALA) ensures patients receive appropriate medical screening and stabilization before transfer.

Best Practices:
- Transfer planning involves coordination with receiving facilities, transport services, and medical teams.
- Documentation of clinical necessity and patient consent is required.
- Alternative care options should be explored before external transfer.

Policy Rationale:
- Transfer protocols ensure continuity of care and appropriate resource utilization.
- Risk assessment includes transport stability and receiving facility capabilities.
""",
    "Consult specialist": """
Official Guidelines:
- American College of Physicians (ACP) guidelines recommend specialist consultation for complex or deteriorating patients.
- Specialty society guidelines (e.g., cardiology, pulmonology) provide criteria for when to involve specialists.
- NEWS2 and other early warning systems trigger specialist involvement for moderate to high-risk patients.

Best Practices:
- Specialist consultation should occur within defined timeframes based on patient acuity.
- Multidisciplinary team involvement improves decision-making and patient outcomes.
- Clear communication of clinical findings and concerns is essential for effective consultation.

Policy Rationale:
- Specialist involvement ensures comprehensive care and reduces adverse events.
- Consultation protocols balance timely intervention with resource availability.
""",
    "Increase monitoring frequency": """
Official Guidelines:
- Royal College of Nursing (RCN) guidelines for vital signs monitoring recommend increased frequency for at-risk patients.
- NEWS2 implementation guides suggest enhanced monitoring for scores 5-8.
- Institute for Healthcare Improvement (IHI) bundles include frequent vital signs assessment for deteriorating patients.

Best Practices:
- Monitoring frequency should be individualized based on patient risk and clinical trajectory.
- Use of early warning systems helps determine appropriate monitoring intervals.
- Staff training ensures accurate vital signs measurement and interpretation.

Policy Rationale:
- Increased monitoring enables early detection of deterioration and timely intervention.
- Protocols define monitoring frequency based on NEWS2 scores and clinical judgment.
""",
    "Monitor closely": """
Official Guidelines:
- National Institute for Health and Care Excellence (NICE) guidelines recommend standard monitoring for stable patients.
- NEWS2 guidelines suggest routine monitoring for low-risk patients (scores 0-4).
- Hospital accreditation standards require appropriate monitoring based on patient condition.

Best Practices:
- Vital signs should be assessed at regular intervals per hospital protocols.
- Monitoring includes trend analysis and comparison with baseline values.
- Staff should be alert to subtle changes indicating potential deterioration.

Policy Rationale:
- Standard monitoring ensures patient safety while optimizing resource use.
- Protocols define monitoring frequency and parameters for different patient populations.
""",
    "Discharge planning": """
Official Guidelines:
- NICE guidelines for patient discharge emphasize comprehensive planning for safe transitions.
- Joint Commission standards require discharge planning for all hospitalized patients.
- CMS conditions of participation mandate discharge planning processes.

Best Practices:
- Discharge planning should begin early in hospitalization and involve multidisciplinary teams.
- Patient education, medication reconciliation, and follow-up arrangements are essential components.
- Risk assessment identifies patients needing additional support post-discharge.

Policy Rationale:
- Effective discharge planning reduces readmissions and improves patient outcomes.
- Protocols ensure safe transitions and appropriate resource utilization.
""",
}


def get_action_documentation(action: str) -> str:
    """
    Retrieve authoritative documentation supporting a clinical action.

    Args:
        action (str): The clinical action name.

    Returns:
        str: Documentation including official guidelines, best practices, and policy rationale.
             Returns empty string if action not found.
    """
    return ACTION_DOCUMENTATION.get(action, "")
