"""
PDS (Persona Drift Suppressor) - Adaptive Self-Correction

Implements two-stage correction strategy as described in paper Section 4.3.

Note: Case-guided rewriting prompt engineering details (how to construct
exemplar demonstrations and instruct style learning) are in paper Appendix D.
"""

from typing import List, Dict, Optional


class PDSCorrector:
    """
    Adaptive drift correction mechanism
    
    Strategies:
    - Early-stage: L-only hard constraint fallback
    - Mature-stage: PCR case-guided rewriting
    """
    
    def __init__(self, llm_client, pcr_manager, threshold=0.6):
        """
        Initialize PDS corrector
        
        Args:
            llm_client: LLM for response rewriting
            pcr_manager: PCR for case retrieval
            threshold: PCC trigger threshold (paper uses 0.6)
        """
        self.llm_client = llm_client
        self.pcr = pcr_manager
        self.threshold = threshold
    
    def correct_if_needed(self, pcc_score: float, response: str,
                          persona_traits: Dict, current_state: Dict,
                          event: str, scene: str) -> Tuple[str, bool]:
        """
        Apply correction if PCC below threshold
        
        Args:
            pcc_score: Current PCC score
            response: Original low-scoring response
            persona_traits: L-layer traits
            current_state: Current S/M configuration
            event: Event description
            scene: Scene category for PCR retrieval
        
        Returns:
            corrected_response: Rewritten or original response
            was_corrected: Whether correction was applied
        """
        if pcc_score >= self.threshold:
            return response, False  # No correction needed
        
        # Retrieve similar high-quality cases
        similar_cases = self.pcr.retrieve(
            scene=scene,
            event=event,
            state=current_state,
            top_k=3  # Paper Section 4.3 specifies top-3
        )
        
        if len(similar_cases) == 0:
            # Early-stage strategy: L-only correction
            corrected = self._l_only_correction(
                response, persona_traits, current_state, event
            )
        else:
            # Mature-stage strategy: Case-guided correction
            corrected = self._case_guided_correction(
                response, persona_traits, current_state, event, similar_cases
            )
        
        return corrected, True
    
    def _l_only_correction(self, response, traits, state, event):
        """
        Early-stage correction using only L-layer constraints
        
        Prompt design: Prioritize trait preservation over state nuance
        Complete prompt in paper Appendix D, Section D.5.1
        """
        # Construct L-only correction prompt
        # NOTE: Exact prompt wording in paper Appendix D
        
        prompt_template = """
        You are a persona consistency expert. Rewrite the following response
        to ensure character trait compliance.
        
        [Character Traits]
        {traits}
        
        [Current State]
        S={s}, M_meaning={mm}, M_strain={ms}
        
        [Event]
        {event}
        
        [Original Response (violates traits)]
        {response}
        
        [Rewriting Requirements]
        - Maintain ALL L-layer traits
        - Match emotion to S value
        - Reflect M values appropriately
        
        [See paper Appendix D for complete requirements]
        
        Rewritten response:
        """
        
        # Simplified implementation
        # Actual prompt includes detailed trait-checking instructions
        
        corrected = self.llm_client.generate(
            prompt=prompt_template.format(
                traits=self._format_traits(traits),
                s=state['S'],
                mm=state['M_meaning'],
                ms=state['M_strain'],
                event=event,
                response=response
            ),
            temperature=0.7
        )
        
        return corrected
    
    def _case_guided_correction(self, response, traits, state, event, cases):
        """
        Mature-stage correction with PCR case guidance
        
        Key innovation: Instruct LLM to learn behavioral strategies
        from exemplars rather than copy surface patterns.
        
        Complete prompt engineering (how to format cases, how to instruct
        strategy learning) specified in paper Appendix D, Section D.5.2.
        """
        # Format retrieved cases for demonstration
        case_examples = self._format_cases_for_prompt(cases)
        
        # Construct case-guided prompt
        # NOTE: Critical prompt design details in paper Appendix D
        # Includes: how to prevent mechanical copying, how to emphasize
        # learning expression patterns, etc.
        
        prompt_template = """
        Rewrite with reference to high-quality cases.
        
        [Character Traits]
        {traits}
        
        [Current State]
        {state}
        
        [Original Response]
        {response}
        
        [Retrieved High-Quality Cases]
        {cases}
        
        [Rewriting Instructions]
        LEARN the expression patterns from cases (not copy content).
        
        [See paper Appendix D.5.2 for complete instructions]
        
        Rewritten response:
        """
        
        # Simplified implementation
        corrected = self.llm_client.generate(
            prompt=prompt_template.format(
                traits=self._format_traits(traits),
                state=state,
                response=response,
                cases=case_examples
            ),
            temperature=0.7
        )
        
        return corrected
    
    def _format_cases_for_prompt(self, cases: List[Dict]) -> str:
        """
        Format retrieved cases for in-context demonstration
        
        Note: Specific formatting strategy (how to present S/M values,
        how to highlight relevant patterns) detailed in paper Appendix D.
        """
        # Simplified version
        formatted = []
        for i, case in enumerate(cases[:3]):  # Top-3
            formatted.append(f"""
            Case {i+1}:
            Event: {case['event']}
            State: S={case['S']}, M_meaning={case['Mm']}, M_strain={case['Ms']}
            Response: {case['response']}
            """)
        
        return "\n".join(formatted)
    
    def _format_traits(self, traits):
        """Format traits for prompt"""
        return f"{traits['innate']}\n{traits['learned']}\n{traits['currently']}"
