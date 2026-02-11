"""
L/M/S Hierarchical State Tracker

Implements cumulative state evolution as described in paper Section 4.1.

Note: M-layer discretization (9-bucket system) details are in paper Section 4.1.1.
This implementation provides the framework structure.
"""

from typing import Dict, Tuple


class StateTracker:
    """
    Tracks L/M/S psychological states across interactions
    
    - L-layer: Time-invariant traits (loaded from config)
    - M-layer: Mid-term meaning/strain (cumulative updates)
    - S-layer: Short-term affect (cumulative updates)
    """
    
    def __init__(self, persona_config: Dict):
        """
        Initialize state tracker with persona configuration
        
        Args:
            persona_config: JSON config with L-layer traits and initial S/M
        """
        # L-layer (immutable)
        self.L_traits = {
            'innate': persona_config['innate_traits'],
            'learned': persona_config['learned_traits'],
            'currently': persona_config['currently']
        }
        
        # M/S-layer (mutable, initialized from config)
        initial = persona_config.get('initial_state', {})
        self.S = initial.get('s_score', 5.0)
        self.M_meaning = initial.get('m_meaning', 5.0)
        self.M_strain = initial.get('m_strain', 5.0)
        
        # History tracking
        self.state_history = []
    
    def update_state(self, event: str, llm_client) -> Tuple[float, float, float]:
        """
        Update S/M states based on event psychological impact
        
        Args:
            event: Event description
            llm_client: LLM for impact assessment
        
        Returns:
            delta_S, delta_M_meaning, delta_M_strain
        
        Note: Event impact assessment prompt details in paper Appendix D
        """
        # Assess psychological impact (see paper Section 4.1.2)
        deltas = self._assess_psychological_impact(event, llm_client)
        
        # Cumulative update with clipping
        self.S = self._clip(self.S + deltas['S'], 0, 10)
        self.M_meaning = self._clip(self.M_meaning + deltas['M_meaning'], 0, 10)
        self.M_strain = self._clip(self.M_strain + deltas['M_strain'], 0, 10)
        
        # Record history
        self.state_history.append({
            'S': self.S,
            'M_meaning': self.M_meaning,
            'M_strain': self.M_strain,
            'deltas': deltas
        })
        
        return deltas['S'], deltas['M_meaning'], deltas['M_strain']
    
    def get_current_state(self) -> Dict:
        """Get current S/M configuration"""
        return {
            'S': self.S,
            'M_meaning': self.M_meaning,
            'M_strain': self.M_strain
        }
    
    def get_L_traits(self) -> Dict:
        """Get immutable L-layer traits"""
        return self.L_traits
    
    def _assess_psychological_impact(self, event, llm_client):
        """
        Assess event's psychological impact on S/M dimensions
        
        Prompt engineering details in paper Appendix D.
        Returns delta values in range [-2.0, +2.0].
        
        Implementation note: Actual prompt includes L-layer conditioning
        to ensure identical events affect different personas differently.
        """
        # Construct impact assessment prompt
        # NOTE: Complete prompt specification in paper Appendix D
        
        prompt_template = """
        Assess psychological impact of this event on:
        - S (short-term emotion): -2.0 to +2.0
        - M_meaning (purpose/value): -2.0 to +2.0  
        - M_strain (stress): -2.0 to +2.0
        
        Event: {event}
        Persona traits: {traits}
        
        Output format: S=X.X Mm=Y.Y Ms=Z.Z
        
        [Full rubric and examples in paper Appendix D]
        """
        
        # Call LLM for impact assessment
        # Simplified placeholder - actual implementation uses detailed rubric
        result = llm_client.generate(
            prompt=prompt_template.format(
                event=event,
                traits=self.L_traits
            ),
            temperature=0.3
        )
        
        # Parse deltas (simplified)
        # Actual implementation includes validation and bounds checking
        return {
            'S': 0.0,          # Placeholder
            'M_meaning': 0.0,   # Placeholder
            'M_strain': 0.0     # Placeholder
        }
    
    def _clip(self, value, min_val, max_val):
        """Clip value to [min_val, max_val] range"""
        return max(min_val, min(max_val, value))
    
    def get_m_state_description(self) -> str:
        """
        Convert M-layer numerical values to semantic description
        
        Implementation note: Complete 9-bucket discretization mapping
        provided in paper Section 4.1.1. This shows simplified version.
        """
        # Simplified 3-level categorization (actual uses 3x3 grid)
        if self.M_meaning > 6.6:
            meaning_level = "high"
        elif self.M_meaning > 3.3:
            meaning_level = "medium"
        else:
            meaning_level = "low"
        
        if self.M_strain > 6.6:
            strain_level = "high"
        elif self.M_strain > 3.3:
            strain_level = "medium"
        else:
            strain_level = "low"
        
        # NOTE: Complete semantic descriptions for all 9 buckets
        # are specified in paper Section 4.1.1
        
        descriptions = {
            ("high", "low"): "Clear goals but manageable stress",
            ("medium", "medium"): "Moderate purpose and pressure",
            ("low", "high"): "Questioning meaning under high strain",
            # ... other 6 buckets (see paper for complete mapping)
        }
        
        return descriptions.get((meaning_level, strain_level), "Balanced state")
