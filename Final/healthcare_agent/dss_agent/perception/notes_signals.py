from ..models import PatientBeliefState

def get_notes_signals(belief_state: PatientBeliefState) -> dict:
    """
    Placeholder for extracting signals from clinical notes using an LLM.
    In this deterministic module, we just pass through pre-loaded note signals.
    """
    return belief_state.notes_signals
