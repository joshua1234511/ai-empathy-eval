import os, pandas as pd, numpy as np
from scipy.stats import f_oneway

def ensure_dirs():
    os.makedirs("data/outputs", exist_ok=True)
    os.makedirs("data/metrics", exist_ok=True)

def compute_metrics():
    ensure_dirs()
    scen = pd.read_csv("data/scenarios.csv")
    raw = pd.read_csv("data/outputs/raw_model_outputs.csv")
    df = raw.merge(scen[["scenario_id","group_id","reference_decision"]], on="scenario_id", how="left")

    # Accuracy per (scenario, model)
    df["is_correct"] = np.where(
        (df["reference_decision"].isin(["A","B"])) & (df["decision"] == df["reference_decision"]), 1,
        np.where(df["reference_decision"].isin(["A","B"]), 0, np.nan)
    )

    # Consistency: within each (model, group_id), % of mode decision across members
    def consistency(group):
        vals = group["decision"].dropna().tolist()
        if not vals: return np.nan
        mode = pd.Series(vals).mode()
        mode = mode.iloc[0] if not mode.empty else None
        return 100.0 * (sum(v==mode for v in vals) / len(vals)) if mode else np.nan

    cons = df.groupby(["model","group_id"]).apply(consistency).reset_index(name="consistency_group_pct")
    cons_avg = cons.groupby("model")["consistency_group_pct"].mean().reset_index().rename(columns={"consistency_group_pct":"consistency_index_pct"})

    # Empathy & Explanation templates (to be filled by human raters later)
    ratings_path = "data/ratings_template.csv"
    if not os.path.exists(ratings_path):
        df_r = df[["scenario_id","model","decision","rationale"]].drop_duplicates()
        df_r["empathy_rating_1to5"] = ""
        df_r["explanation_rating_1to5"] = ""
        df_r.to_csv(ratings_path, index=False)

    # Aggregate metrics per model
    agg = df.groupby("model").agg(
        decision_accuracy_pct=("is_correct", lambda s: 100.0*np.nanmean(s) if s.notna().any() else np.nan)
    ).reset_index().merge(cons_avg, on="model", how="left")

    # After you collect ratings, join them in
    if os.path.exists("data/ratings_filled.csv"):
        r = pd.read_csv("data/ratings_filled.csv")
        r["empathy_rating_1to5"] = pd.to_numeric(r["empathy_rating_1to5"], errors="coerce")
        r["explanation_rating_1to5"] = pd.to_numeric(r["explanation_rating_1to5"], errors="coerce")
        ragg = r.groupby("model").agg(
            empathy_alignment_1to5=("empathy_rating_1to5", "mean"),
            explanation_quality_1to5=("explanation_rating_1to5", "mean"),
        ).reset_index()
        agg = agg.merge(ragg, on="model", how="left")

        # Per-scenario for ANOVA
        per = r.merge(df[["scenario_id","model","is_correct"]], on=["scenario_id","model"], how="left")
        per["accuracy"] = per["is_correct"]
        per_metrics_path = "data/metrics/metrics_per_scenario_per_model.csv"
        per.to_csv(per_metrics_path, index=False)
    else:
        per_metrics_path = None

    agg_path = "data/metrics/metrics_per_model.csv"
    agg.to_csv(agg_path, index=False)
    return {"metrics_per_model": agg_path, "metrics_per_scenario_per_model": per_metrics_path}

def prepare_tables():
    # Table A
    agg = pd.read_csv("data/metrics/metrics_per_model.csv")
    table_a = agg.rename(columns={
        "decision_accuracy_pct": "Decision Accuracy (%)",
        "empathy_alignment_1to5": "Empathy Alignment Score (1–5)",
        "explanation_quality_1to5": "Explanation Quality (1–5)",
        "consistency_index_pct": "Consistency Index (%)"
    })
    table_a_path = "data/results_table_A.csv"
    table_a.to_csv(table_a_path, index=False)

    # Table B (ANOVA) requires filled ratings + per-scenario metrics
    table_b_path = "data/results_table_B.csv"
    if os.path.exists("data/metrics/metrics_per_scenario_per_model.csv"):
        per = pd.read_csv("data/metrics/metrics_per_scenario_per_model.csv")
        rows = []
        for metric in ["accuracy", "empathy_rating_1to5", "explanation_rating_1to5"]:
            groups = [g[metric].dropna().values for _, g in per.groupby("model")]
            if all(len(g)>1 for g in groups):
                from scipy.stats import f_oneway
                stat, p = f_oneway(*groups)
                rows.append({"Metric": metric, "F-Statistic": stat, "p-Value": p, "Significant Difference (p < 0.05)?": "Yes" if p<0.05 else "No"})
        pd.DataFrame(rows).to_csv(table_b_path, index=False)
    else:
        pd.DataFrame([{"Metric":"accuracy","F-Statistic":"","p-Value":"","Significant Difference (p < 0.05)?":""}]).to_csv(table_b_path, index=False)

    # Table C sample
    table_c_path = "data/results_table_C.csv"
    raw = pd.read_csv("data/outputs/raw_model_outputs.csv") if os.path.exists("data/outputs/raw_model_outputs.csv") else pd.DataFrame(columns=["scenario_id","model","decision","rationale"])
    if os.path.exists("data/ratings_filled.csv"):
        r = pd.read_csv("data/ratings_filled.csv")
        merged = raw.merge(r[["scenario_id","model","empathy_rating_1to5"]], on=["scenario_id","model"], how="left")
        sample = merged.sort_values("empathy_rating_1to5", ascending=False).head(3)
    else:
        sample = raw.head(3)
    sample.rename(columns={"rationale":"Reasoning Summary","empathy_rating_1to5":"Expert Empathy Rating"}, inplace=True)
    sample.to_csv(table_c_path, index=False)

    return {"table_a": table_a_path, "table_b": table_b_path, "table_c": table_c_path}
