# Model orchestration for backend API
# Adapt this to use your llm_runner and pipeline code

def run_all_models(scenario_text, additional_data=None):
    # TODO: Integrate with models.llm_runner and eval.pipeline
    # For now, return dummy data for all models
    return [
        {'model': 'gptj', 'decision': 'A', 'rationale': 'Sample rationale for GPT-J', 'accuracy': 1.0},
        {'model': 'llama2', 'decision': 'B', 'rationale': 'Sample rationale for LLaMA 2', 'accuracy': 0.0},
        {'model': 'bloomz', 'decision': 'A', 'rationale': 'Sample rationale for BLOOMZ', 'accuracy': 1.0},
        {'model': 'tree', 'decision': 'B', 'rationale': 'Sample rationale for Decision Tree', 'accuracy': 0.0},
        {'model': 'forest', 'decision': 'A', 'rationale': 'Sample rationale for Random Forest', 'accuracy': 1.0},
    ]
