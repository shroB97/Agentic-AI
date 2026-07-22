from app.workflows.ap_workflow import process_invoices


def main() -> None:
    print("\nAGENTIC AI AP EXCEPTION MANAGEMENT")
    print("=" * 50)

    decisions = process_invoices()

    for decision in decisions:
        print(f"\nInvoice: {decision.invoice_id}")
        print(f"Exceptions: {decision.exception_types or ['NONE']}")
        print(f"Variance: {decision.variance_percent}")
        print(f"Risk score: {decision.risk_score}")
        print(f"Route: {decision.route}")
        print(f"Explanation: {decision.explanation}")


if __name__ == "__main__":
    main()
