from app.models.invoice import Invoice, Vendor


RISK_LEVEL_SCORES = {
    "LOW": 5,
    "MEDIUM": 20,
    "HIGH": 45,
    "UNKNOWN": 35,
}


def calculate_risk_score(
    invoice: Invoice,
    vendor: Vendor | None,
    exception_types: list[str],
    is_duplicate: bool,
) -> int:
    score = 0

    if vendor is None:
        score += 40
    else:
        score += RISK_LEVEL_SCORES.get(vendor.risk_level.upper(), 25)

        if not vendor.active:
            score += 30

        if vendor.bank_change_pending:
            score += 40

    if is_duplicate:
        score += 60

    if "MISSING_PO" in exception_types:
        score += 20

    if "PO_NOT_FOUND" in exception_types:
        score += 25

    if "VENDOR_MISMATCH" in exception_types:
        score += 35

    if "AMOUNT_VARIANCE" in exception_types:
        score += 15

    return min(score, 100)


def determine_route(
    risk_score: int,
    exception_types: list[str],
) -> str:
    if "DUPLICATE_INVOICE" in exception_types:
        return "FRAUD_OR_COMPLIANCE_REVIEW"

    if risk_score >= 70:
        return "FRAUD_OR_COMPLIANCE_REVIEW"

    if risk_score >= 40:
        return "SENIOR_FINANCE_REVIEW"

    if exception_types:
        return "AP_SPECIALIST_REVIEW"

    return "AUTO_APPROVE"
