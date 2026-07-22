import streamlit as st

from app.agents.exception_investigation_agent import investigate_decision
from app.workflows.ap_workflow import process_invoices


st.set_page_config(
    page_title="Agentic AI AP Exception Manager",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Agentic AI AP Exception Management")
st.caption(
    "Deterministic financial controls with AI-assisted investigation"
)

st.markdown(
    """
This application detects invoice exceptions, calculates risk,
routes invoices through financial controls, and generates
AI-assisted investigation recommendations.
"""
)

try:
    decisions = process_invoices()
except Exception as exc:
    st.error(f"Unable to load invoice decisions: {exc}")
    st.stop()

invoice_ids = [
    f"{decision.invoice_id} — {decision.route}"
    for decision in decisions
]

selected_label = st.selectbox(
    "Select an invoice",
    invoice_ids,
)

selected_index = invoice_ids.index(selected_label)
decision = decisions[selected_index]

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Risk Score",
        decision.risk_score,
    )

with col2:
    st.metric(
        "Variance",
        (
            f"{decision.variance_percent}%"
            if decision.variance_percent is not None
            else "N/A"
        ),
    )

with col3:
    st.metric(
        "Route",
        decision.route.replace("_", " ").title(),
    )

st.subheader("Deterministic Assessment")

st.write(f"**Invoice ID:** {decision.invoice_id}")
st.write(
    "**Exceptions:** "
    + (
        ", ".join(decision.exception_types)
        if decision.exception_types
        else "None"
    )
)
st.write(f"**Explanation:** {decision.explanation}")

if decision.route == "AUTO_APPROVE":
    st.success(
        "This invoice passed the configured checks and can proceed "
        "through the auto-approval route."
    )
else:
    st.warning(
        "This invoice requires human review. AI may assist with "
        "investigation, but it cannot override the mandatory route."
    )

st.divider()

st.subheader("AI Investigation")

run_ai = st.button(
    "Run AI Investigation",
    type="primary",
    disabled=decision.route == "AUTO_APPROVE",
)

if decision.route == "AUTO_APPROVE":
    st.info("AI investigation is skipped for auto-approved invoices.")

if run_ai:
    with st.spinner("Investigating invoice exception..."):
        try:
            recommendation = investigate_decision(decision)

            priority = recommendation.priority

            if priority == "CRITICAL":
                st.error(f"Priority: {priority}")
            elif priority == "HIGH":
                st.warning(f"Priority: {priority}")
            else:
                st.info(f"Priority: {priority}")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.write(
                    "**Recommended action:** "
                    f"{recommendation.recommended_action}"
                )
                st.write(
                    "**Human review required:** "
                    f"{recommendation.human_review_required}"
                )

            with result_col2:
                st.write(
                    "**Confidence:** "
                    f"{recommendation.confidence:.0%}"
                )
                st.write(
                    "**Mandatory route:** "
                    f"{decision.route}"
                )

            st.write("**Rationale**")
            st.write(recommendation.rationale)

            st.write("**Required actions**")

            for action in recommendation.required_actions:
                st.markdown(f"- {action}")

        except Exception as exc:
            st.error("AI investigation failed.")
            st.code(str(exc))
            st.warning(
                "The deterministic routing decision remains authoritative."
            )

st.divider()

st.subheader("Process Control Design")

st.markdown(
    """
1. Validate the invoice against purchase-order data.
2. Detect amount variances and duplicate invoices.
3. calculate the vendor-related risk score.
4. Assign a mandatory deterministic route.
5. Use AI only to recommend investigation actions.
6. Preserve human approval for controlled exceptions.
"""
)
