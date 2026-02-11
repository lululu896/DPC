# Data Format Specifications

## Persona Configuration (JSON)

```json
{
  "name": "String - Persona identifier",
  "age": "Integer",
  "occupation": "String",
  "innate_traits": "String - Core personality traits",
  "learned_traits": "String - Acquired behavioral patterns",
  "currently": "String - Current life context",
  "lifestyle": "String - Daily routines and preferences",
  "initial_state": {
    "s_score": "Float 0-10 - Initial affect",
    "m_meaning": "Float 0-10 - Initial meaningfulness",
    "m_strain": "Float 0-10 - Initial stress level"
  }
}
```

## Experimental Output (CSV)

Generated results include the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `persona` | String | Persona name |
| `seed` | Integer | Random seed for reproducibility |
| `event` | String | Event description |
| `S_value` | Float | Affect state at generation time |
| `M_meaning` | Float | Meaningfulness state |
| `M_strain` | Float | Stress state |
| `response` | String | Generated response text |
| `L_score` | Float | L-layer stability score (0-1) |
| `S_score` | Float | S-layer alignment score (0-1) |
| `M_score` | Float | M-layer coherence score (0-1) |
| `PCC_original` | Float | PCC before correction |
| `PCC_rewritten` | Float | PCC after correction (if applied) |
| `was_rewritten` | Boolean | Whether PDS intervened |

## PCR Case Structure (JSON)

```json
{
  "scene_category": [
    {
      "id": "String - Unique case identifier",
      "event": "String - Event description",
      "response": "String - High-quality response",
      "S": "Float - Affect state",
      "Mm": "Float - Meaningfulness",
      "Ms": "Float - Stress",
      "pcc_score": "Float - Quality score (>=0.85)",
      "embedding": "List[Float] - Dense event vector (1536-dim)",
      "timestamp": "String - Generation time"
    }
  ]
}
```

## State Trajectory Format

For tracking psychological state evolution across interactions:

```json
{
  "persona": "String",
  "seed": "Integer",
  "trajectory": [
    {
      "step": "Integer",
      "event": "String",
      "S_before": "Float",
      "S_after": "Float",
      "M_before": {"meaning": "Float", "strain": "Float"},
      "M_after": {"meaning": "Float", "strain": "Float"},
      "delta_S": "Float (-2.0 to +2.0)",
      "delta_M": {"meaning": "Float", "strain": "Float"}
    }
  ]
}
```

## Notes

- All scores are in range [0, 1] unless otherwise specified
- S/M state values are in range [0, 10]
- Delta values for state updates are in range [-2.0, +2.0]
- Embeddings use OpenAI text-embedding-ada-002 (1536 dimensions)

For complete data schema and examples, see paper Section 5 and Appendices.
