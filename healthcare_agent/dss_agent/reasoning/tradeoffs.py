from typing import List
from ..models import Recommendation

def analyze_tradeoffs(recommendations: List[Recommendation]) -> str:
    """
    Generates a text summary of the tradeoffs between the top recommendations.
    """
    if not recommendations:
        return "No actions recommended."
        
    top = recommendations[0]
    
    summary = f"Recommended: {top.action} (Conf: {top.confidence}). "
    
    if len(recommendations) > 1:
        alt = recommendations[1]
        summary += f"Alternative: {alt.action} has lower score due to "
        if alt.cost.level == "High" and top.cost.level != "High":
             summary += "higher resource cost."
        elif alt.confidence < top.confidence:
             summary += "lower confidence in benefit."
        else:
             summary += "ranking logic."
             
    return summary
