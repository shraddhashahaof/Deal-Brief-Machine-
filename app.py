"""
app.py — Streamlit UI only. All prompt logic lives in prompts.py,
all execution logic lives in chain.py, all settings load from config.py / .env.

Run:
    pip install -r requirements.txt
    cp .env.example .env      # then paste your Groq key into .env
    streamlit run app.py
"""

import streamlit as st

from config import GROQ_API_KEY
from prompts import STEPS, SAMPLE_INPUT
from chain import run_chain

st.set_page_config(page_title="Deal Brief Machine | Fuse Capital Group", layout="wide")

st.title("📋 Deal Brief Machine")
st.caption("Fuse Capital Group — AI Generalist Assignment prototype")

with st.sidebar:
    st.header("Setup")
    if GROQ_API_KEY:
        st.success("API key loaded from .env")
        api_key = GROQ_API_KEY
    else:
        st.warning("No GROQ_API_KEY found in .env")
        api_key = st.text_input(
            "Paste your Groq API key (fallback only — prefer .env)",
            type="password",
            help="Get a free key at console.groq.com/keys",
        )
    st.divider()
    st.markdown("**Workflow steps**")
    for s in STEPS:
        st.markdown(f"- {s['title']}")

st.subheader("1. Paste raw deal intake notes")
raw_input = st.text_area(
    "This is exactly how a deal team would paste notes from an intake call — "
    "unstructured, in whatever order they came up.",
    value=SAMPLE_INPUT,
    height=180,
)

run = st.button("▶ Run Deal Brief Machine", type="primary", disabled=not api_key)
if not api_key:
    st.info("Add GROQ_API_KEY to your .env file (or paste a key above) to run the workflow.")

if run and api_key:
    progress_bar = st.progress(0.0, text="Starting...")

    def on_progress(i, total, title):
        progress_bar.progress(i / total, text=f"Running {title}...")

    outputs = run_chain(api_key, raw_input, STEPS, on_progress=on_progress)
    progress_bar.progress(1.0, text="Done.")

    st.subheader("2. Intermediate reasoning steps")
    # Steps 1-4 are intermediate reasoning, shown as expandable detail.
    # Steps 5 (brief) and 6 (scorecard) together form the final deliverable
    # and are shown once, below — never repeated inside these expanders.
    intermediate_steps, intermediate_outputs = STEPS[:4], outputs[:4]
    brief_output, scorecard_output = outputs[4], outputs[5]

    for step, output in zip(intermediate_steps, intermediate_outputs):
        with st.expander(f"{step['title']} — {step['desc']}", expanded=False):
            st.markdown(output)

    st.subheader("3. Final Deal Brief")
    st.markdown(brief_output)

    st.subheader("4. Risk & Readiness Scorecard")
    st.markdown(scorecard_output)

    full_document = brief_output + "\n\n" + scorecard_output
    st.download_button(
        "⬇ Download Full Deal Brief + Scorecard (.txt)",
        data=full_document,
        file_name="NovaBuild_Deal_Brief.txt",
        mime="text/plain",
    )
