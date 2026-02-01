"""
Module for generating memory-based narrative explanations.
Compares current state to historical state to highlight changes.
"""
from typing import List
from ..models import Vitals

def generate_memory_narrative(history: List[Vitals], current: Vitals) -> List[str]:
    """
    Generates a list of strings describing changes since the last assessment.
    """
    narrative = []
    
    if not history:
        narrative.append("Initial assessment - no prior history.")
        return narrative
        
    last = history[-1]
    
    # Check NEWS2 change
    if current.news2 != last.news2:
        direction = "increased" if current.news2 > last.news2 else "decreased"
        narrative.append(f"NEWS2 score {direction} from {last.news2} -> {current.news2}")
    
    # Check RR change (significant if >= 4 change? or just any change?)
    # Requirement: "Respiratory rate increased from 22 -> 28"
    if abs(current.rr - last.rr) >= 2:
        direction = "increased" if current.rr > last.rr else "decreased"
        narrative.append(f"Respiratory rate {direction} from {last.rr} -> {current.rr}")
        
    # Check SpO2 change
    if abs(current.spo2 - last.spo2) >= 3:
        direction = "dropped" if current.spo2 < last.spo2 else "improved"
        narrative.append(f"SpO2 {direction} from {last.spo2}% -> {current.spo2}%")
        
    # Check SBP change
    if abs(current.sbp - last.sbp) >= 15:
         direction = "dropped" if current.sbp < last.sbp else "rose"
         narrative.append(f"Systolic BP {direction} from {last.sbp} -> {current.sbp}")
         
    # AVPU change
    if current.avpu != last.avpu:
        narrative.append(f"Consciousness level changed from {last.avpu} -> {current.avpu}")

    if not narrative:
        narrative.append("Vital signs remain stable since last assessment.")
        
    return narrative
