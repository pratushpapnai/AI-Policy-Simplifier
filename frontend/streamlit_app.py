import re
import importlib.util
from pathlib import Path
import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "app" / "config.py"
config_spec = importlib.util.spec_from_file_location("policy_simplifier_config", CONFIG_PATH)
config = importlib.util.module_from_spec(config_spec)
config_spec.loader.exec_module(config)

RISK_MAP = config.RISK_MAP
URL = "http://localhost:8000/summarize"


st.set_page_config(
    page_title="Policy Simplifier AI",
    page_icon="PS",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        body {
            background-color: #fffaf5;
        }

        .stApp {
            background: linear-gradient(180deg, #fff7ed 0%, #ffffff 44%, #fffaf5 100%);
            color: #1f2937;
        }

        .main .block-container {
            max-width: 1150px;
            padding-top: 28px;
            padding-bottom: 48px;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #fed7aa;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] li,
        [data-testid="stSidebar"] span {
            color: #1f2937;
        }

        .top-bar {
            background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
            border: 1px solid #fb923c;
            border-radius: 18px;
            padding: 28px 32px;
            margin-bottom: 22px;
            box-shadow: 0 14px 32px rgba(234, 88, 12, 0.22);
        }

        .brand-label {
            display: inline-block;
            color: #9a3412;
            background: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.75);
            border-radius: 999px;
            padding: 6px 12px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 14px;
        }

        .top-bar h1 {
            color: #ffffff;
            font-size: 44px;
            line-height: 1.1;
            margin: 0 0 10px 0;
            letter-spacing: -1px;
        }

        .top-bar p {
            color: rgba(255, 255, 255, 0.92);
            font-size: 17px;
            max-width: 780px;
            margin: 0;
        }

        .section-heading {
            color: #9a3412;
            font-size: 20px;
            font-weight: 800;
            margin: 10px 0 10px 0;
        }

        .info-card {
            background: #ffffff;
            border: 1px solid #fed7aa;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 14px;
            box-shadow: 0 8px 20px rgba(234, 88, 12, 0.08);
        }

        .info-card h3 {
            color: #f97316;
            font-size: 17px;
            margin: 0 0 6px 0;
        }

        .info-card p {
            color: #4b5563;
            font-size: 14px;
            margin: 0;
        }

        .summary-card {
            background: #ffffff;
            border: 1px solid #fed7aa;
            border-left: 6px solid #f97316;
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 12px;
            box-shadow: 0 8px 20px rgba(234, 88, 12, 0.08);
        }

        .summary-card b {
            color: #f97316;
        }

        .summary-card ul {
            margin-bottom: 0;
            padding-left: 20px;
        }

        .summary-card li {
            color: #374151;
            margin: 7px 0;
        }

        .risk-card {
            background: #fff7ed;
            border: 1px solid #fb923c;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 10px;
        }

        .risk-title {
            color: #f97316;
            font-size: 16px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .risk-description {
            color: #4b5563;
            font-size: 14px;
        }

        .evidence {
            background: #ffffff;
            border: 1px solid #fed7aa;
            border-radius: 10px;
            color: #374151;
            padding: 10px 12px;
            margin-top: 8px;
            font-size: 14px;
        }

        div[data-testid="stTextArea"] textarea {
            background: #ffffff;
            border: 1px solid #fb923c;
            border-radius: 14px;
            color: #111827;
            font-size: 15px;
        }

        div[data-testid="stTextArea"] textarea:focus {
            border-color: #f97316;
            box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.18);
        }

        div.stButton > button {
            height: 48px;
            border-radius: 12px;
            border: 1px solid #ea580c;
            background: #f97316;
            color: #ffffff;
            font-size: 16px;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(249, 115, 22, 0.25);
        }

        div.stButton > button:hover {
            background: #ea580c;
            border-color: #c2410c;
            color: #ffffff;
        }

        [data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #fed7aa;
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 8px 20px rgba(234, 88, 12, 0.08);
        }

        [data-testid="stMetric"] label,
        [data-testid="stMetric"] div {
            color: #111827;
        }

        [data-testid="stExpander"] {
            background: #ffffff;
            border: 1px solid #fed7aa;
            border-radius: 14px;
        }

        [data-testid="stExpander"] p,
        [data-testid="stExpander"] span,
        [data-testid="stExpander"] div {
            color: #111827;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.title("Policy Simplifier")
    st.caption("AI-powered privacy policy analysis")
    st.markdown("---")

    st.write("### Model")
    st.success("Fine-tuned Qwen 2.5 1.5B")

    st.write("### Backend")
    st.info("FastAPI + Transformers")

    st.write("### Outputs")
    st.markdown("- Plain-language summary\n- Privacy risk categories\n- Supporting evidence")

    st.markdown("---")
    st.caption("Paste a real policy clause for best results.")


st.markdown(
    """
    <div class="top-bar">
        <span class="brand-label">Policy Simplifier AI</span>
        <h1>Understand policies without reading the fine print.</h1>
        <p>
            Paste a privacy policy or terms section. The app summarizes it in simple language
            and highlights privacy risks with evidence from the text.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


left_col, right_col = st.columns([1.5, 0.8], gap="large")

with left_col:
    st.markdown('<div class="section-heading">Paste your policy</div>', unsafe_allow_html=True)
    policy = st.text_area(
        "Paste Policy",
        label_visibility="collapsed",
        height=290,
        placeholder="Example: We collect your billing address, payment details, transaction history...",
    )
    generate = st.button("Analyze Policy", use_container_width=True)

with right_col:
    st.markdown('<div class="section-heading">What this app returns</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="info-card">
            <h3>Simple summary</h3>
            <p>A short explanation of what the policy says.</p>
        </div>
        <div class="info-card">
            <h3>Risk categories</h3>
            <p>Detected privacy topics such as payment data, location, usage data, and more.</p>
        </div>
        <div class="info-card">
            <h3>Evidence clauses</h3>
            <p>The exact text snippets that support each detected risk.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if generate:
    if policy.strip() == "":
        st.warning("Please paste a policy first.")
        st.stop()

    with st.spinner("Analyzing policy..."):
        try:
            response = requests.post(
                URL,
                json={"text": policy},
                timeout=300,
            )
            response.raise_for_status()

            result = response.json()
            summaries = result["summaries"]
            risks = result["risk_statements"]

        except Exception as e:
            st.error(str(e))
            st.stop()

    detected_risks = {k: v for k, v in risks.items() if len(v) != 0}
    total_evidence = sum(len(v) for v in detected_risks.values())

    st.success("Analysis complete.")

    metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
    metric_col_1.metric("Summary chunks", len(summaries))
    metric_col_2.metric("Risk categories", len(detected_risks))
    metric_col_3.metric("Evidence clauses", total_evidence)

    st.markdown('<div class="section-heading">Plain-language summary</div>', unsafe_allow_html=True)

    if len(summaries) == 0:
        st.info("No summary was returned. Please check whether the backend received non-empty policy text.")

    for index, summary in enumerate(summaries, start=1):
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", summary) if s.strip()]
        bullet_items = "".join(f"<li>{sentence}</li>" for sentence in sentences)
        st.markdown(
            f"""
            <div class="summary-card">
                <b>Summary chunk {index}</b>
                <ul>{bullet_items}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-heading">Privacy risks found</div>', unsafe_allow_html=True)

    if len(detected_risks) == 0:
        st.success("No privacy risks were detected in this text.")
    else:
        for category, evidence_items in detected_risks.items():
            with st.expander(f"{category} - {len(evidence_items)} evidence clause(s)", expanded=True):
                st.markdown(
                    f"""
                    <div class="risk-card">
                        <div class="risk-title">{category}</div>
                        <div class="risk-description">{RISK_MAP.get(category, category)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for evidence in evidence_items:
                    st.markdown(
                        f'<div class="evidence">"{evidence}"</div>',
                        unsafe_allow_html=True,
                    )
