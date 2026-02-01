from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class RiskLevel(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

@dataclass
class Vitals:
    avpu: str = "A"
    sbp: int = 120
    spo2: int = 98
    rr: int = 16
    hr: int = 80
    temp: float = 37.0
    news2: int = 0
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class PatientBeliefState:
    patient_id: str
    current_vitals: Vitals
    history: List[Vitals] = field(default_factory=list)
    active_interventions: List[str] = field(default_factory=list)
    # Extracted signals from notes (simulated for now)
    notes_signals: Dict[str, str] = field(default_factory=dict) 

@dataclass
class ResourceState:
    icu_beds_available: int
    rrt_available: bool
    nurse_load: float  # 0.0 to 1.0 (or >1.0 if overloaded)
    transport_delay_minutes: int
    specialist_available: bool = True

@dataclass
class Cost:
    level: str  # "Low", "Medium", "High"
    explanation: str

@dataclass
class Recommendation:
    action: str
    rationale: str
    expected_benefit: str
    cost: Cost
    confidence: float
    emergent: bool
    rank: int = 0
    counterfactual_analysis: Optional[Dict[str, Any]] = field(default=None)
    
    def to_dict(self):
        return {
            "action": self.action,
            "rationale": self.rationale,
            "expected_benefit": self.expected_benefit,
            "cost": {
                "level": self.cost.level,
                "explanation": self.cost.explanation
            },
            "confidence": self.confidence,
            "emergent": self.emergent,
            "rank": self.rank,
            "counterfactual_analysis": self.counterfactual_analysis
        }
