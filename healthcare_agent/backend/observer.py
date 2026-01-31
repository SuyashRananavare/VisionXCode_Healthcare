"""
ReAct-Style Observer for Deterministic Agent

This module provides a function to format deterministic reasoning traces
in a clear, human-readable ReAct-style format: Thought → Observation → Conclusion.

"""


def format_react_reasoning(reasoning_trace: str) -> str:
    """
    Format a deterministic reasoning trace in ReAct-style format.

    Args:
        reasoning_trace (str): The raw reasoning trace from the agent.

    Returns:
        str: Formatted reasoning in Thought → Observation → Conclusion format.
    """
    # Split the trace into steps (assuming it's structured)
    steps = reasoning_trace.split("\n")
    formatted = []
    for step in steps:
        if "Thought:" in step:
            formatted.append(step)
        elif "Observation:" in step:
            formatted.append(step)
        elif "Conclusion:" in step:
            formatted.append(step)
        else:
            # If not structured, wrap as Observation
            formatted.append(f"Observation: {step}")
    return "\n".join(formatted)

