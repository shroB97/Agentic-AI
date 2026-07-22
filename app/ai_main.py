from app.agents.exception_investigation_agent import investigate_decision
from app.workflows.ap_workflow import process_invoices


def main() -> None:
    print("\nAI-ENABLED AP EXCEPTION INVESTIGATION")
    print("=" * 55)

    decisions = process_invoices()

    for decision in decisions:
        print(f"\nInvoice: {decision.invoice_id}")
        print(f"Deterministic route: {decision.route}")

        if decision.route == "AUTO_APPROVE":
            print("AI investigation: skipped")
            print("Reason: No exception investigation is required.")
            continue

        try:
            recommendation = investigate_decision(decision)

            print(f"AI recommendation: {recommendation.recommended_action}")
            print(f"Priority: {recommendation.priority}")
            print(
                f"Human review required: "
                f"{recommendation.human_review_required}"
            )
            print(f"Confidence: {recommendation.confidence}")
            print(f"Rationale: {recommendation.rationale}")
            print("Required actions:")

            for action in recommendation.required_actions:
                print(f"- {action}")

        except Exception as exc:
            print("AI investigation failed.")
            print(f"Error: {exc}")
            print(
                "The deterministic route remains authoritative: "
                f"{decision.route}"
            )


if __name__ == "__main__":
    main()
