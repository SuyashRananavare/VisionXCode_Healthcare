# Clinical Decision Support System - Refactored Agent

## Overview

This module implements an agentic Decision Support System (DSS) for hospital patient escalation. It is designed to be:
- **Modular**: Components are separated into Perception, World Model, and Reasoning layers.
- **Deterministic**: Outcomes are based on explicit rules and scoring logic, ensuring safety and explainability.
- **Agentic**: It maintains state over time (`PatientBeliefState`) and reasons about resource constraints.

## Architecture

The system follows an `Observe -> Update Beliefs -> Reason -> Recommend` loop.

### 1. World Model (`dss_agent.world_model`)
Maintains the current state of the patient (vitals history) and the hospital resources (beds, staff).

### 2. Perception (`dss_agent.perception`)
Extracts actionable signals from raw data:
- `vitals_trends`: Detects instability (e.g., rapid SBP drop).
- `delay_signals`: Identifies overdue reviews.

### 3. Reasoning (`dss_agent.reasoning`)
- **Safety**: Hard-coded overrides for critical conditions (e.g., Call RRT if SBP < 70).
- **Scoring**: Ranks actions based on risk, benefit, and resource cost.
- **Tradeoffs**: Analyzes alternatives.

### 4. Agent (`dss_agent.agent`)
Orchestrates the components.

## Usage

```python
from dss_agent.agent import EscalationAgent
from dss_agent.models import Vitals, ResourceState

agent = EscalationAgent(patient_id="123")
vitals = Vitals(sbp=85, news2=7)
resources = ResourceState(icu_beds_available=1, ...)

recommendations = agent.run_step(vitals, resources)
print(recommendations[0]['action'])
```

## Verification

Run the scenario script to see the agent in action across a patient trajectory:

```bash
python run_scenario.py
```
