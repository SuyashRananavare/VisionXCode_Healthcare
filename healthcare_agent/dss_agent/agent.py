from typing import List, Dict, Any
from .models import Vitals, ResourceState, Recommendation
from .world_model import WorldModel
from .perception import vitals_trends, delay_signals, treatment_response, notes_signals
from .reasoning import safety, scoring, tradeoffs, counterfactual, narrative

class EscalationAgent:
    def __init__(self, patient_id: str):
        self.world_model = WorldModel(patient_id)
        # Defined possible actions (configuration)
        self.possible_actions = [
            {"action": "Monitor closely", "base_score": 0.4, "benefit": "Low", "cost_level": "Low", "cost_exp": "Minimal", "min_risk": 0.0},
            {"action": "Increase monitoring frequency", "base_score": 0.6, "benefit": "Medium", "cost_level": "Low", "cost_exp": "Nursing time", "min_risk": 0.1},
            {"action": "Consult specialist", "base_score": 0.7, "benefit": "Medium", "cost_level": "Medium", "cost_exp": "Specialist time", "min_risk": 0.2},
            {"action": "ICU transfer", "base_score": 0.9, "benefit": "High", "cost_level": "High", "cost_exp": "ICU bed", "min_risk": 0.3},
            {"action": "Prepare transfer plan / bed request", "base_score": 0.8, "benefit": "Medium", "cost_level": "Medium", "cost_exp": "Admin coordination", "min_risk": 0.3},
            {"action": "Discharge planning", "base_score": 0.2, "benefit": "Low", "cost_level": "Low", "cost_exp": "Planning time", "min_risk": 0.0},
        ]

    def run_step(self, new_vitals: Vitals, resource_state: ResourceState) -> List[Dict[str, Any]]:
        """
        Executes one cycle of the agent loop:
        Observe -> Update Beliefs -> Reason -> Recommend
        """
        # 1. Update Beliefs (World Model)
        self.world_model.update_vitals(new_vitals)
        self.world_model.update_resources(resource_state)
        
        belief_state = self.world_model.patient_belief
        
        # 2. Perception (Extract Signals)
        # These signals could be attached to belief_state or passed to reasoning
        trend_signals = vitals_trends.analyze_vital_trends(belief_state.history, belief_state.current_vitals)
        delay_sig = delay_signals.check_delays(belief_state)
        response_sig = treatment_response.check_treatment_response(belief_state)
        
        # 3. Reason (Generate Recommendations)
        # A. Safety Check (Hard overrides)
        emergent_rec = safety.check_safety_rules(belief_state)
        if emergent_rec:
            return [emergent_rec.to_dict()]
            
        # B. Scoring & Ranking
        recommendations = scoring.score_actions(belief_state, resource_state, self.possible_actions)
        
        # C. Tradeoff Analysis (could be added to metadata)
        # tradeoff_summary = tradeoffs.analyze_tradeoffs(recommendations)
        
        # Limit to top 3
        top_recs = recommendations[:3]
        
        # D. Counterfactual Analysis (Explanation)
        # Collect signals
        explanation_signals = []
        explanation_signals.extend(trend_signals.get("trends", []))
        if delay_sig.get("overdue_review"):
            explanation_signals.append("overdue_review")
        if emergent_rec:
            explanation_signals.append("emergent_safety_trigger")

        # Estimate risk from NEWS2 (0-20 scale mapped to 0-1)
        current_risk = min(1.0, belief_state.current_vitals.news2 / 20.0)

        # Determine Intent
        # Default to escalate if emergent or if top recommendation is high score/high cost
        # Monitor if top recommendation is "Monitor closely" or scores are low
        
        primary_rec = top_recs[0]
        intent = "escalate"
        next_check_in = None
        
        # Threshold for escalation: standard score threshold or specific action types
        # If the top action is "Monitor closely" or "Increase monitoring frequency"
        # AND it's not emergent, we consider it a MONITORING intent.
        
        monitoring_actions = ["Monitor closely", "Increase monitoring frequency", "Discharge planning"]
        
        if not emergent_rec:
            if primary_rec.action in monitoring_actions:
                 intent = "monitor"
                 # Set check-in time based on action
                 if primary_rec.action == "Increase monitoring frequency":
                     next_check_in = 30 # Check sooner
                 else:
                     next_check_in = 60 # Standard check
            elif primary_rec.confidence < 0.5: # Low confidence in escalation
                 # Force intent to monitor if confidence in escalation is low? 
                 # Maybe safer to stick to recommendation but flag intent.
                 pass

        # Generate Memory Narrative
        narrative_lines = narrative.generate_memory_narrative(belief_state.history, belief_state.current_vitals)

        for rec in top_recs:
            # Propagate intent to all (or just primary? Usually intent is agent-level)
            # But we persist it on the recommendation objects as requested.
            rec.intent = intent
            if intent == "monitor":
                rec.next_check_in_minutes = next_check_in
            
            rec.memory_narrative = narrative_lines

            cf_result = counterfactual.analyze_counterfactual(
                current_risk=current_risk,
                delay_minutes=next_check_in if next_check_in else 60,
                active_signals=explanation_signals
            )
            rec.counterfactual_analysis = cf_result

        return [rec.to_dict() for rec in top_recs]
