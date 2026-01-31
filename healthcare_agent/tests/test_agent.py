"""
Unit tests for healthcare agent recommendation module.

Tests cover 6 scenarios as specified:
1. Stable patient
2. Slow decline
3. Rapid deterioration
4. Noisy false alarm
5. Post-op fever
6. Emergent physiology

Also tests ICU bed constraints and deterministic output.
"""

import pytest
from backend.agent import generate_recommendations


class TestHealthcareAgent:
    """Test suite for healthcare agent recommendations."""

    def test_stable_patient(self):
        """Test recommendations for a stable patient with low NEWS2."""
        patient = {"AVPU": "A", "SBP": 120, "SpO2": 98, "RR": 16, "NEWS2": 2}
        resource_state = {
            "icu_beds_available": 2,
            "rrt_available": True,
            "nurse_load": 0.5,
            "transport_delay": 15,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not be emergent
        assert not any(rec["emergent"] for rec in recommendations)

        # Should include monitoring or discharge actions
        actions = [rec["action"] for rec in recommendations]
        assert "Monitor closely" in actions or "Discharge planning" in actions

        # Confidence should be reasonable
        for rec in recommendations:
            assert 0.3 <= rec["confidence"] <= 0.8

    def test_slow_decline(self):
        """Test recommendations for patient with moderate NEWS2 indicating slow decline."""
        patient = {"AVPU": "A", "SBP": 110, "SpO2": 95, "RR": 18, "NEWS2": 5}
        resource_state = {
            "icu_beds_available": 1,
            "rrt_available": True,
            "nurse_load": 0.6,
            "transport_delay": 20,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not be emergent
        assert not any(rec["emergent"] for rec in recommendations)

        # Should include increased monitoring or consultation
        actions = [rec["action"] for rec in recommendations]
        assert (
            "Increase monitoring frequency" in actions
            or "Consult specialist" in actions
        )

        # Confidence should be moderate
        for rec in recommendations:
            assert 0.5 <= rec["confidence"] <= 1.0

    def test_rapid_deterioration(self):
        """Test recommendations for patient with high NEWS2 but not meeting safety threshold."""
        patient = {"AVPU": "A", "SBP": 100, "SpO2": 92, "RR": 22, "NEWS2": 8}
        resource_state = {
            "icu_beds_available": 1,
            "rrt_available": True,
            "nurse_load": 0.7,
            "transport_delay": 10,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not be emergent
        assert not any(rec["emergent"] for rec in recommendations)

        # Should include ICU transfer or specialist consultation
        actions = [rec["action"] for rec in recommendations]
        assert "ICU transfer" in actions or "Consult specialist" in actions

        # Confidence should be higher
        for rec in recommendations:
            assert 0.7 <= rec["confidence"] <= 1.0

    def test_noisy_false_alarm(self):
        """Test recommendations for patient with elevated NEWS2 but normal vitals."""
        patient = {"AVPU": "A", "SBP": 130, "SpO2": 97, "RR": 14, "NEWS2": 7}
        resource_state = {
            "icu_beds_available": 3,
            "rrt_available": True,
            "nurse_load": 0.4,
            "transport_delay": 5,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not be emergent
        assert not any(rec["emergent"] for rec in recommendations)

        # Should focus on monitoring rather than aggressive actions
        actions = [rec["action"] for rec in recommendations]
        assert (
            "Monitor closely" in actions or "Increase monitoring frequency" in actions
        )

        # Confidence should be moderate
        for rec in recommendations:
            assert 0.5 <= rec["confidence"] <= 1.0

    def test_post_op_fever(self):
        """Test recommendations for post-operative patient with fever."""
        patient = {"AVPU": "A", "SBP": 115, "SpO2": 96, "RR": 20, "NEWS2": 4}
        resource_state = {
            "icu_beds_available": 2,
            "rrt_available": True,
            "nurse_load": 0.5,
            "transport_delay": 15,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not be emergent
        assert not any(rec["emergent"] for rec in recommendations)

        # Should include increased monitoring
        actions = [rec["action"] for rec in recommendations]
        assert "Increase monitoring frequency" in actions

        # Confidence should be reasonable
        for rec in recommendations:
            assert 0.4 <= rec["confidence"] <= 0.8

    def test_emergent_physiology(self):
        """Test recommendations for patient meeting safety criteria."""
        patient = {
            "AVPU": "V",  # Not alert
            "SBP": 65,  # Hypotensive
            "SpO2": 85,  # Hypoxic
            "RR": 30,  # Tachypneic
            "NEWS2": 12,  # High score
        }
        resource_state = {
            "icu_beds_available": 1,
            "rrt_available": True,
            "nurse_load": 0.9,  # High load, but should ignore for emergent
            "transport_delay": 25,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should have emergent RRT call as first recommendation
        assert recommendations[0]["action"] == "Call RRT"
        assert recommendations[0]["emergent"] is True
        assert recommendations[0]["confidence"] >= 0.85

        # Should mention safety criteria in rationale
        assert "critical safety criteria" in recommendations[0]["rationale"]

    def test_icu_bed_constraint(self):
        """Test that ICU transfer is not recommended when no beds available."""
        patient = {"AVPU": "A", "SBP": 100, "SpO2": 92, "RR": 22, "NEWS2": 8}
        resource_state = {
            "icu_beds_available": 0,  # No beds
            "rrt_available": True,
            "nurse_load": 0.7,
            "transport_delay": 10,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should not recommend ICU transfer
        actions = [rec["action"] for rec in recommendations]
        assert "ICU transfer" not in actions

        # Should recommend transfer plan instead
        assert "Prepare transfer plan / bed request" in actions

    def test_deterministic_output(self):
        """Test that output is deterministic for same inputs."""
        patient = {"AVPU": "A", "SBP": 110, "SpO2": 95, "RR": 18, "NEWS2": 5}
        resource_state = {
            "icu_beds_available": 1,
            "rrt_available": True,
            "nurse_load": 0.6,
            "transport_delay": 20,
        }

        # Run multiple times
        recs1 = generate_recommendations(patient, resource_state)
        recs2 = generate_recommendations(patient, resource_state)
        recs3 = generate_recommendations(patient, resource_state)

        # Should be identical
        assert recs1 == recs2 == recs3

        # Check specific fields are identical
        for i in range(len(recs1)):
            assert recs1[i]["action"] == recs2[i]["action"]
            assert recs1[i]["confidence"] == recs2[i]["confidence"]
            assert recs1[i]["emergent"] == recs2[i]["emergent"]

    def test_max_three_recommendations(self):
        """Test that at most 3 recommendations are returned."""
        patient = {
            "AVPU": "A",
            "SBP": 120,
            "SpO2": 98,
            "RR": 16,
            "NEWS2": 10,  # High risk
        }
        resource_state = {
            "icu_beds_available": 2,
            "rrt_available": True,
            "nurse_load": 0.5,
            "transport_delay": 15,
        }

        recommendations = generate_recommendations(patient, resource_state)

        assert len(recommendations) <= 3

    def test_emergent_with_other_recommendations(self):
        """Test that emergent recommendation is included with other recommendations."""
        patient = {
            "AVPU": "A",
            "SBP": 60,  # Triggers emergent
            "SpO2": 98,
            "RR": 16,
            "NEWS2": 8,
        }
        resource_state = {
            "icu_beds_available": 2,
            "rrt_available": True,
            "nurse_load": 0.5,
            "transport_delay": 15,
        }

        recommendations = generate_recommendations(patient, resource_state)

        # Should start with RRT call
        assert recommendations[0]["action"] == "Call RRT"
        assert recommendations[0]["emergent"] is True

        # Should have additional recommendations
        assert len(recommendations) >= 2
