import argparse
from models.llm_runner import run_models_on_scenarios
from eval.pipeline import compute_metrics, prepare_tables, ensure_dirs

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--models", type=str, default="gptj,bloomz")
    p.add_argument("--scenarios", type=str, default="data/scenarios.csv")
    args = p.parse_args()

    ensure_dirs()
    selected = [m.strip() for m in args.models.split(",") if m.strip()]
    raw = run_models_on_scenarios(args.scenarios, selected)
    print(f"Raw outputs: {raw}")
    m = compute_metrics()
    print(m)
    t = prepare_tables()
    print(t)

if __name__ == "__main__":
    main()
