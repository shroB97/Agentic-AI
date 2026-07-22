import os

from agents import Agent, Runner
from dotenv import load_dotenv

from app.models.decision import AgentRecommendation, ProcessDecision


load_dotenv()


def build_exception_investigation_agent() -> Agent:
    model_name = os.getenv("OPENAI_MODEL", "gpt-5-mini")

    return Agent(
        name="AP Exception Investigation Agent",
        model=model_name,
        instructions=(
            "You are an Accounts Payable exception investigation specialist. "
            "Review deterministic invoice validation findings and provide a "
            "controlled recommendation. "
            "\n\n"
            "Rules:"
            "\n1. Never claim that payment has been executed."
            "\n2. Never override the deterministic workflow route."
            "\n3. Duplicate invoices must require fraud or compliance review."
            "\n4. Pending vendor bank-detail changes require human review."
            "\n5. Missing purchase orders require documentation or AP review."
            "\n6. High-risk vendors require senior finance review."
            "\n7. Explain the recommendation using only the supplied findings."
            "\n8. Do not invent invoice, vendor, policy, or purchase-order data."
            "\n9. Return concise, auditable actions."
        ),
        output_type=AgentRecommendation,
    )


def investigate_decision(
    decision: ProcessDecision,
) -> AgentRecommendation:
    agent = build_exception_investigation_agent()

    prompt = f"""
Review the following deterministic Accounts Payable decision.

Invoice ID: {decision.invoice_id}
Exception types: {decision.exception_types}
Variance percent: {decision.variance_percent}
Risk score: {decision.risk_score}
Mandatory workflow route: {decision.route}
Rule-based explanation: {decision.explanation}

Provide an investigation recommendation.
The recommended action must not weaken or bypass the mandatory workflow route.
"""

    result = Runner.run_sync(agent, prompt)

    return result.final_output
