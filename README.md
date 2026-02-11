# DPC
Beyond Static Persona Consistency: Dynamic Persona Coherence in LLM Role-Playing

P³ Framework: Dynamic Persona Coherence via Hierarchical Psychological State Modeling
This repository provides the core framework implementation for our ACL 2026 submission on dynamic persona coherence in LLM-based role-playing agents.

📋 Overview
Traditional LLM role-playing systems treat personas as monolithic static entities, conflating stable identity traits with transient psychological states. Our P³ framework (Persona with Persistent Psychological states) addresses this via:

L/M/S Hierarchical Model: Separating long-term traits (L), mid-term resilience (M), and short-term affect (S)
PCC (Persona Consistency Critic): Three-dimensional decomposed evaluation with evidence grounding
PDS (Persona Drift Suppressor): Adaptive self-correction via case-guided rewriting
PCR (Persona Case Repository): Selective high-quality exemplar accumulation
⚠️ Important Notes
This is a minimal reproducibility package designed to demonstrate our method's core architecture. For full implementation details including:

Exact prompt engineering specifications
Hyperparameter tuning procedures
Complete experimental analysis scripts
Detailed evaluation rubrics
Please refer to the paper Appendices C-D. We will release the complete codebase including all optimization details upon paper acceptance.

🚀 Quick Start
Installation
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Running a Simple Experiment
from core.framework import P3Framework

# Initialize framework
framework = P3Framework(
    persona_config="config/personas/lisa_chen.json",
    llm_provider="openai",
    pcc_model="gpt-4o"
)

# Run single interaction
event = "Received critical feedback on work quality"
response = framework.generate_response(event)
pcc_score = framework.evaluate_response(response, event)

print(f"Generated Response: {response}")
print(f"PCC Score: {pcc_score}")
📊 Reproducing Paper Results
python run_experiment.py --persona lisa_chen --model gpt-4o --seeds 204,205,206,207,208
📁 Repository Structure
public_release/
├── config/           # Persona configurations
├── core/             # Core framework components
├── prompts/          # Prompt templates (see paper for details)
├── utils/            # Utility functions
└── outputs/          # Experimental results (generated)
🔧 What's Included
✅ Core framework architecture (PCC, PDS, PCR)
✅ L/M/S state tracking mechanisms
✅ Example persona configurations
✅ Basic experiment runner
✅ Data format specifications
🔧 What's Simplified
⚠️ Prompt templates: Framework provided, exact wording in paper Appendix D
⚠️ Evaluation rubrics: Structure shown, detailed criteria in Appendix C
⚠️ Hyperparameters: Values reported in Section 5.1
⚠️ Analysis tools: Available upon request after acceptance
📖 Citation
@inproceedings{anonymous2026p3,
  title={Dynamic Persona Coherence via Hierarchical Psychological State Modeling},
  author={Anonymous Authors},
  booktitle={Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (ACL 2026)},
  year={2026}
}
🔒 Code Availability
Complete codebase with full prompt specifications, hyperparameter tuning scripts, and analysis tools will be released upon paper acceptance.
