from app.models.invoice import Invoice, PurchaseOrder


def calculate_variance_percent(
    invoice_amount: float,
    po_amount: float,
) -> float:
    if po_amount <= 0:
        raise ValueError("PO amount must be greater than zero.")

    variance = ((invoice_amount - po_amount) / po_amount) * 100
    return round(variance, 2)


def validate_invoice_against_po(
    invoice: Invoice,
    purchase_order: PurchaseOrder | None,
) -> tuple[list[str], float | None]:
    exceptions: list[str] = []

    if not invoice.po_number:
        exceptions.append("MISSING_PO")
        return exceptions, None

    if purchase_order is None:
        exceptions.append("PO_NOT_FOUND")
        return exceptions, None

    if purchase_order.status != "OPEN":
        exceptions.append("PO_NOT_OPEN")

    if invoice.vendor_id != purchase_order.vendor_id:
        exceptions.append("VENDOR_MISMATCH")

    if invoice.currency != purchase_order.currency:
        exceptions.append("CURRENCY_MISMATCH")

    variance_percent = calculate_variance_percent(
        invoice.invoice_amount,
        purchase_order.po_amount,
    )

    if abs(variance_percent) > 5:
        exceptions.append("AMOUNT_VARIANCE")

    return exceptions, variance_percent
