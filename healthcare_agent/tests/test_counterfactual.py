import pytest
from dss_agent.reasoning.counterfactual import analyze_counterfactual

def test_analyze_counterfactual_base():
    """Test base risk increase with no signals."""
    current_risk = 0.1
    delay = 60
    active_signals = []
    
    result = analyze_counterfactual(current_risk, delay, active_signals)
    
    # Base rate 0.001 * 60 = 0.06
    expected_increase = 0.06
    assert result["projected_risk"] == pytest.approx(0.16)
    assert result["risk_change"] == pytest.approx(0.06)
    assert not result["key_drivers"]
    assert "baseline" in result["summary"]

def test_analyze_counterfactual_with_signals():
    """Test risk increase with high risk signals."""
    current_risk = 0.2
    delay = 60
    # "rapid_deterioration" multiplier is 3.0
    active_signals = ["active_bleeding", "rapid_deterioration"] 
    # "active_bleeding" is not in dict, should be ignored for multiplier but maybe listed? 
    # Logic in counterfactual.py checks: if signal in SIGNAL_MULTIPLIERS.
    
    result = analyze_counterfactual(current_risk, delay, active_signals)
    
    # Rate = 0.001 * 3.0 = 0.003
    # Increase = 0.003 * 60 = 0.18
    # Projected = 0.2 + 0.18 = 0.38
    
    assert result["projected_risk"] == pytest.approx(0.38)
    assert "rapid_deterioration" in result["key_drivers"]
    assert "Driven by" in result["summary"]

def test_analyze_counterfactual_cap():
    """Test that risk is capped at 1.0."""
    current_risk = 0.9
    delay = 200 # Long delay
    active_signals = ["emergent_safety_trigger"] # Multiplier 5.0
    
    # Rate = 0.001 * 5.0 = 0.005
    # Increase = 0.005 * 200 = 1.0
    # Projected raw = 1.9 -> Cap 1.0
    
    result = analyze_counterfactual(current_risk, delay, active_signals)
    
    assert result["projected_risk"] == 1.0
    assert result["risk_change"] == pytest.approx(0.1) # 1.0 - 0.9
    assert "maximum critical level" in result["summary"] or "critical saturation" in result["summary"]

def test_analyze_counterfactual_custom_signals():
    """Test with signals mapped from agent."""
    current_risk = 0.1
    delay = 60
    active_signals = ["Rapid SBP drop", "overdue_review"]
    
    # Rapid SBP drop multiplier 2.5
    # overdue_review multiplier 1.5
    # Should take max = 2.5
    
    result = analyze_counterfactual(current_risk, delay, active_signals)
    
    # Rate = 0.001 * 2.5 = 0.0025
    # Increase = 0.0025 * 60 = 0.15
    # Projected = 0.25
    
    assert result["projected_risk"] == pytest.approx(0.25)
    assert "Rapid SBP drop" in result["key_drivers"]
