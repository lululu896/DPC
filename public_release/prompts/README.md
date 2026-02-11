# Prompt Templates

This directory provides the **structural templates** for our framework's prompts. Complete prompt engineering specifications, including exact wording, evaluation rubrics, and instruction phrasing, are detailed in the paper's Appendix D.

## Template Overview

### 1. Response Generation Prompt
- **Purpose**: Generate persona responses conditioned on L-layer traits and current S/M states
- **Structure**: See `generation_template.txt`
- **Complete specification**: Paper Appendix D, Section D.3

### 2. PCC Evaluation Prompt
- **Purpose**: Three-dimensional coherence assessment with evidence grounding
- **Structure**: See `evaluation_template.txt`
- **Complete specification**: Paper Appendix D, Section D.4

### 3. PDS Correction Prompts
- **Purpose**: Self-correction via L-only or case-guided rewriting
- **Structure**: See `correction_template.txt`
- **Complete specification**: Paper Appendix D, Section D.5

## ⚠️ Important

The templates provided here show the **architectural framework**. Critical implementation details preserved for post-acceptance release include:

- Exact NLI guidance phrasing
- Evidence extraction instruction specifics  
- Case demonstration formatting strategies
- Trait-checking rubric details

These details significantly impact system performance and represent our core prompt engineering contributions. Reviewers can verify our approach's validity through the complete prompts in paper Appendix D, while implementation subtleties will be shared upon acceptance to support reproducibility.

## 📖 Usage

To use these templates in your own implementation:

1. Load template file
2. Fill placeholders with persona-specific content
3. Refer to paper Appendix D for detailed prompt construction guidelines
4. Tune phrasing based on your specific LLM provider

For exact prompts used in our experiments, see paper Appendix D.
