"""
P³ Framework Core Components
ACL 2026 Anonymous Submission

This package contains the core implementation of:
- PCC (Persona Consistency Critic)
- PDS (Persona Drift Suppressor)  
- PCR (Persona Case Repository)
- L/M/S State Tracking

For detailed algorithm specifications, see paper Sections 4.1-4.3.
"""

__version__ = "0.1.0"
__author__ = "Anonymous"

from .pcc_evaluator import PCCEvaluator
from .pds_corrector import PDSCorrector
from .pcr_manager import PCRManager
from .state_tracker import StateTracker

__all__ = [
    "PCCEvaluator",
    "PDSCorrector",
    "PCRManager",
    "StateTracker",
]
