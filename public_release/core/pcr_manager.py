"""
PCR (Persona Case Repository) - Selective Exemplar Library

Implements dual-index retrieval as described in paper Section 4.3.1.

Note: Exact retrieval weighting (λ=0.6) and scene categorization
details are specified in paper Section 4.3.1.
"""

import json
import numpy as np
from typing import List, Dict, Optional


class PCRManager:
    """
    Manages high-quality response exemplars for PDS guidance
    
    Dual-index retrieval:
    - Semantic similarity (event embeddings)
    - Psychological state proximity (S/M distance)
    
    RankScore = λ * semantic_sim + (1-λ) * state_proximity
    """
    
    def __init__(self, storage_path: str = "data/pcr_repository.json"):
        """
        Initialize PCR manager
        
        Args:
            storage_path: Path to PCR JSON file
        """
        self.storage_path = storage_path
        self.repository = self._load_or_create()
        
        # Universal scene categories (paper Section 4.3.1)
        self.scenes = [
            "authority_interaction",
            "peer_interaction", 
            "task_execution",
            "conflict_resolution"
        ]
    
    def add_case(self, scene: str, event: str, response: str,
                 state: Dict, pcc_score: float, embedding: List[float]):
        """
        Add high-quality case to repository
        
        Admission criterion: PCC >= 0.85 (paper Section 4.3.1)
        
        Args:
            scene: Interaction category
            event: Event description
            response: High-scoring response
            state: S/M configuration at time of generation
            pcc_score: PCC score (must be >= 0.85)
            embedding: Dense semantic vector of event
        """
        if pcc_score < 0.85:
            return  # Only admit high-quality cases
        
        case = {
            'event': event,
            'response': response,
            'S': state['S'],
            'Mm': state['M_meaning'],
            'Ms': state['M_strain'],
            'pcc_score': pcc_score,
            'embedding': embedding
        }
        
        if scene not in self.repository:
            self.repository[scene] = []
        
        self.repository[scene].append(case)
        self._save()
    
    def retrieve(self, scene: str, event: str, state: Dict,
                 top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-K most relevant cases
        
        Dual-index ranking (paper Equation in Section 4.3.1):
        RankScore = λ * CosineSim(event_q, event_c) + (1-λ) * StateProximity
        
        Args:
            scene: Scene category for coarse filtering
            event: Query event description
            state: Query state (S, M_meaning, M_strain)
            top_k: Number of cases to return
        
        Returns:
            Top-K ranked cases
        
        Note: λ weighting and StateProximity normalization details
        are specified in paper Section 4.3.1.
        """
        if scene not in self.repository or len(self.repository[scene]) == 0:
            return []
        
        # Get event embedding for semantic similarity
        event_embedding = self._get_embedding(event)
        
        # Rank all cases in this scene
        ranked_cases = []
        for case in self.repository[scene]:
            # Semantic similarity (cosine)
            semantic_sim = self._cosine_similarity(
                event_embedding, case['embedding']
            )
            
            # Psychological state proximity
            # NOTE: Normalization factor (30.0) derivation in paper Section 4.3.1
            state_proximity = self._compute_state_proximity(state, case)
            
            # Weighted combination
            # NOTE: λ=0.6 determined via ablation (paper Section 5.3)
            LAMBDA = 0.6  # See paper for justification
            rank_score = LAMBDA * semantic_sim + (1 - LAMBDA) * state_proximity
            
            ranked_cases.append({
                **case,
                'rank_score': rank_score
            })
        
        # Sort and return top-K
        ranked_cases.sort(key=lambda x: x['rank_score'], reverse=True)
        return ranked_cases[:top_k]
    
    def _compute_state_proximity(self, query_state, case):
        """
        Compute psychological state proximity
        
        Uses L1 distance normalized by maximum possible distance (30.0).
        See paper Section 4.3.1 for formula.
        """
        distance = (
            abs(query_state['S'] - case['S']) +
            abs(query_state['M_meaning'] - case['Mm']) +
            abs(query_state['M_strain'] - case['Ms'])
        )
        
        # Normalize and convert to proximity
        # Max distance = 30.0 (three dimensions, each 0-10)
        proximity = 1.0 - (distance / 30.0)
        
        return proximity
    
    def _cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between embeddings"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        
        if norm_product == 0:
            return 0.0
        
        return dot_product / norm_product
    
    def _get_embedding(self, text):
        """
        Get dense embedding for text
        
        Paper uses OpenAI text-embedding-ada-002
        Placeholder implementation - integrate with your embedding service
        """
        # Placeholder - replace with actual embedding API call
        return [0.0] * 1536
    
    def _load_or_create(self):
        """Load existing repository or create empty"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {scene: [] for scene in self.scenes}
    
    def _save(self):
        """Save repository to disk"""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.repository, f, ensure_ascii=False, indent=2)
