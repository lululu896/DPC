# Frequently Asked Questions

## General Questions

### Q: Is this the complete codebase from your paper?

**A**: This is a minimal reproducibility package showing our framework's core architecture. Complete implementation including all prompt engineering details, hyperparameter tuning scripts, and analysis tools will be released upon paper acceptance. Reviewers can verify our approach through the complete specifications in paper Appendices C-D.

### Q: How do I reproduce your exact experimental results?

**A**: 
1. Use the persona configurations in `config/personas/`
2. Follow the experimental protocol in paper Section 5.1
3. Apply prompts as specified in paper Appendix D
4. Use hyperparameters from paper Section 5.1 (PCC threshold=0.6, PCR admission=0.85, λ=0.6, etc.)

The framework code here provides the architectural structure. Exact prompts and tuned parameters are in the paper.

### Q: Why are some implementation details simplified?

**A**: To protect core intellectual contributions during anonymous review while maintaining reproducibility. Key innovations (prompt engineering strategies, evaluation rubric design, case demonstration techniques) are fully documented in the paper and will be released in complete form upon acceptance.

## Technical Questions

### Q: Which LLM should I use for PCC evaluation?

**A**: Paper uses GPT-4o for all PCC evaluations to ensure consistent judging standards across different generation models. See paper Section 5.1.

### Q: What's the difference between `PCC_original` and `PCC_rewritten`?

**A**: 
- `PCC_original`: Score of initially generated response (with S/M tracking but before PDS)
- `PCC_rewritten`: Score after PDS correction (if triggered)

This enables ablation analysis (Section 5.3): comparing +S/M alone vs. +S/M+PDS.

### Q: How many exemplars should PCR contain before PDS becomes effective?

**A**: Paper Section 5.3 shows PDS effectiveness improves as PCR grows. Early-stage (0-10 cases) uses L-only fallback. Mature-stage (30+ cases) achieves consistent high-quality corrections.

### Q: What are the four universal scenes?

**A**: 
1. Authority interaction (criticism, guidance, evaluation)
2. Peer interaction (collaboration, social invitations)
3. Task execution (work activities, problem-solving)
4. Conflict resolution (disputes, disagreements)

See paper Section 4.3.1.

## Reproducibility Questions

### Q: Can I reproduce Table 1 from the paper with this code?

**A**: The framework structure is provided, but exact reproduction requires:
- Complete prompts (paper Appendix D)
- Tuned hyperparameters (paper Section 5.1)
- Event sequences (paper Appendix A)
- All 5 persona configurations (3 provided here, 2 more in paper Appendix)

We provide sufficient detail in the paper for reproduction. Complete codebase post-acceptance will facilitate easier replication.

### Q: How do I handle API rate limits?

**A**: Implement exponential backoff and batch processing. Our experiments process ~100-150 events per persona with appropriate rate limiting (details available upon request).

### Q: What computational resources are required?

**A**: 
- No GPU required (all LLM calls are API-based)
- Approx. 8-12 minutes per 100-event sequence
- API costs: ~$2-5 per persona-seed configuration (using GPT-4o)

See paper Section 5.1 for complete resource specifications.

## Contact

For questions not covered here, please:
1. Refer to paper Sections 4-5 and Appendices
2. Open an issue in this repository
3. Contact via anonymous submission portal

---

**Note**: This FAQ will be expanded with additional implementation guidance upon paper acceptance.
