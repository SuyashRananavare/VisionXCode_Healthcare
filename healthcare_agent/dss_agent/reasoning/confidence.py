def calibrate_confidence(raw_score: float, risk_level: float, missing_info: float = 0.0) -> float:
    """
    Calibrates confidence score based on uncertainty and risk.
    """
    # Conservative calibration: high risk should increase confidence in ACTION,
    # but missing info should decrease it.
    
    confidence = raw_score
    
    # If risk is very high, we are more confident that *something* needs to be done.
    if risk_level > 0.8:
        confidence = min(confidence * 1.2, 1.0)
        
    # Penalize for missing info
    confidence = confidence * (1.0 - missing_info)
    
    return round(confidence, 2)
