# Healthcare Agent Recommendation Module

## Overview

This module implements a deterministic, auditable agent for generating clinical recommendations in a hospital AI system. It replaces heuristic planners with a rule-based system that prioritizes patient safety and resource awareness.

## Logic Overview

### 1. Safety Rules (Priority 1)
The agent first checks mandatory safety criteria:
- AVPU ≠ "A" (not alert)
- SBP < 70 mmHg (hypotensive)
- SpO₂ < 80% (hypoxic)
- RR > 35 breaths/min (tachypneic)
- NEWS2 ≥ 9 (high early warning score)

If any criteria are met, immediately recommend "Call RRT" with emergent=True and confidence ≥ 0.85.

### 2. Risk Assessment
- Base risk = NEWS2 score normalized to 0-1 (NEWS2/20)
- Actions have minimum risk thresholds for consideration
- Higher risk increases action scores

### 3. Resource Constraints
- **ICU Beds**: If `icu_beds_available == 0`, skip ICU transfer; recommend "Prepare transfer plan / bed request" instead
- **Nurse Load**: If `nurse_load > 0.9`, penalize high-cost actions (unless emergent)
- **Transport Delay**: Penalizes ICU transfer score based on delay time

### 4. Action Scoring
Each action has:
- Base score (0-1)
- Risk adjustment (+ base_risk * 0.4)
- Resource penalties
- Minimum risk threshold

Actions are ranked by final score, returning top 1-3 recommendations.

### 5. Confidence Calculation
Confidence = min(score * (1 + base_risk) / 2, 1.0)
- Higher scores and risk increase confidence
- Conservative calibration ensures explainability

## Key Features

- **Deterministic**: Same inputs always produce same outputs
- **Fast**: Pure Python with O(1) complexity
- **Auditable**: Clear scoring logic with no randomness
- **Resource-Aware**: Considers bed availability, staffing, and delays
- **Safety-First**: Hard-coded emergency triggers
- **Explainable**: Each recommendation includes rationale mentioning key drivers

## API

```python
def generate_recommendations(patient: dict, resource_state: dict) -> list[dict]:
    # Returns 1-3 ranked recommendations
```

### Input Formats
- **patient**: Dict with vitals (AVPU, SBP, SpO2, RR, NEWS2)
- **resource_state**: Dict with icu_beds_available, rrt_available, nurse_load, transport_delay

### Output Format
Each recommendation dict contains:
- `action`: String description
- `rationale`: 1-2 sentence explanation
- `expected_benefit`: "High" | "Medium" | "Low"
- `cost`: {"level": "High"|"Medium"|"Low", "explanation": string}
- `confidence`: Float 0.0-1.0
- `emergent`: Bool (True only for immediate actions)

## Testing

Run unit tests with pytest:
```bash
pytest tests/test_agent.py
```

Tests cover 6 clinical scenarios plus edge cases for deterministic behavior and resource constraints.