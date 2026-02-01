from datetime import datetime
from typing import Optional, List
from .models import PatientBeliefState, ResourceState, Vitals

class WorldModel:
    """
    Manages the agent's belief about the world, including patient state
    and resource availability.
    """
    def __init__(self, patient_id: str):
        self.patient_belief = PatientBeliefState(
            patient_id=patient_id,
            current_vitals=Vitals(),
            history=[]
        )
        self.resource_state: Optional[ResourceState] = None
        self.last_assessment_time: Optional[datetime] = None
        self.last_recommendation: Optional[dict] = None

    def update_vitals(self, new_vitals: Vitals):
        """
        Updates the patient's current vitals and archives the previous state
        to history.
        """
        # Archive current vitals to history if it's not the initial empty state
        # or if we want to track every update. 
        # For simplicity, we'll append the *previous* current_vitals to history.
        if self.patient_belief.current_vitals.timestamp != new_vitals.timestamp:
             self.patient_belief.history.append(self.patient_belief.current_vitals)
        
        # Update current vitals
        self.patient_belief.current_vitals = new_vitals
        self.last_assessment_time = datetime.now()

    def update_resources(self, new_resources: ResourceState):
        """
        Updates the agent's knowledge of hospital resources.
        """
        self.resource_state = new_resources

    def get_history(self) -> List[Vitals]:
        return self.patient_belief.history

    def get_current_vitals(self) -> Vitals:
        return self.patient_belief.current_vitals
