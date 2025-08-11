import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from models.llm_runner import run_models_on_scenarios
from eval.pipeline import compute_metrics, prepare_tables, ensure_dirs

load_dotenv()

st.set_page_config(page_title="AI Empathy Eval", layout="wide")
st.title("AI Empathy Eval — Scenario Runner & Tables")

ensure_dirs()

SCENARIO_PATH = "data/scenarios.csv"

# --- Sidebar: Model selection ---
st.sidebar.header("Models")
use_gptj = st.sidebar.checkbox("GPT-J (6B)", value=True)
use_bloomz = st.sidebar.checkbox("BLOOMZ (7B1)", value=True)
use_llama2 = st.sidebar.checkbox("LLaMA 2 (7B)", value=False)
use_tree = st.sidebar.checkbox("Decision Tree (baseline)", value=False)
use_forest = st.sidebar.checkbox("Random Forest (baseline)", value=False)

# --- Scenario editor ---
st.subheader("Add / Edit Scenarios")
if not os.path.exists(SCENARIO_PATH):
    pd.DataFrame(columns=[
        "scenario_id","group_id","scenario_text","reference_decision","tags","notes"
    ]).to_csv(SCENARIO_PATH, index=False)

df = pd.read_csv(SCENARIO_PATH)

with st.form("add_form"):
    st.markdown("**Add new scenario**")
    scenario_id = st.text_input("Scenario ID (e.g., 1a)", value="")
    group_id = st.text_input("Group ID for consistency (e.g., 1)", value="")
    scenario_text = st.text_area("Scenario text (A/B options should be clear)", height=160)
    reference_decision = st.selectbox("Reference decision (optional)", ["", "A", "B"])
    tags = st.text_input("Tags (comma separated)", value="")
    notes = st.text_area("Notes (optional)", height=60)
    submitted = st.form_submit_button("Add scenario")
    if submitted:
        if scenario_id and scenario_text:
            df = pd.concat([df, pd.DataFrame([{
                "scenario_id": scenario_id,
                "group_id": group_id,
                "scenario_text": scenario_text,
                "reference_decision": reference_decision,
                "tags": tags,
                "notes": notes
            }])], ignore_index=True)
            df.to_csv(SCENARIO_PATH, index=False)
            st.success(f"Added scenario {scenario_id}")
        else:
            st.error("Scenario ID and text are required.")

st.markdown("**Current Scenarios**")
st.dataframe(df, use_container_width=True)

# --- Run section ---
st.subheader("Run Models")
if st.button("Run selected models on all scenarios"):
    selected = []
    if use_gptj: selected.append("gptj")
    if use_bloomz: selected.append("bloomz")
    if use_llama2: selected.append("llama2")
    if use_tree: selected.append("tree")
    if use_forest: selected.append("forest")
    if not selected:
        st.error("Please select at least one model.")
    else:
        with st.spinner("Running models..."):
            raw_path = run_models_on_scenarios("data/scenarios.csv", selected)
        st.success(f"Done. Raw outputs saved to {raw_path}")

# --- Compute metrics and prep tables ---
st.subheader("Metrics & Tables")
if st.button("Compute metrics and prepare Tables A/B/C"):
    paths = compute_metrics()
    tpaths = prepare_tables()
    st.success("Metrics & tables generated.")
    st.write(paths)
    st.write(tpaths)

st.info("Outputs are written to data/outputs and data/metrics. Tables are saved to data/results_table_*.csv")
