from collections import Counter

import pandas as pd

from app.models.decision import ProcessDecision
from app.models.invoice import Invoice, PurchaseOrder, Vendor
from app.tools.matching_tools import validate_invoice_against_po
from app.tools.risk_tools import calculate_risk_score, determine_route


def load_business_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    invoices = pd.read_csv("data/invoices.csv")
    purchase_orders = pd.read_csv("data/purchase_orders.csv")
    vendors = pd.read_csv("data/vendors.csv")

    return invoices, purchase_orders, vendors


def find_purchase_order(
    po_number: str | None,
    purchase_orders: pd.DataFrame,
) -> PurchaseOrder | None:
    if not po_number:
        return None

    matches = purchase_orders[purchase_orders["po_number"] == po_number]

    if matches.empty:
        return None

    return PurchaseOrder(**matches.iloc[0].to_dict())


def find_vendor(
    vendor_id: str,
    vendors: pd.DataFrame,
) -> Vendor | None:
    matches = vendors[vendors["vendor_id"] == vendor_id]

    if matches.empty:
        return None

    return Vendor(**matches.iloc[0].to_dict())


def process_invoices() -> list[ProcessDecision]:
    invoices_df, purchase_orders_df, vendors_df = load_business_data()

    invoice_counts = Counter(invoices_df["invoice_id"].tolist())
    processed_ids: set[str] = set()
    decisions: list[ProcessDecision] = []

    for _, row in invoices_df.iterrows():
        raw_invoice = row.to_dict()

        if pd.isna(raw_invoice.get("po_number")):
            raw_invoice["po_number"] = None

        invoice = Invoice(**raw_invoice)

        purchase_order = find_purchase_order(
            invoice.po_number,
            purchase_orders_df,
        )

        vendor = find_vendor(
            invoice.vendor_id,
            vendors_df,
        )

        exception_types, variance_percent = validate_invoice_against_po(
            invoice,
            purchase_order,
        )

        is_duplicate = (
            invoice_counts[invoice.invoice_id] > 1
            and invoice.invoice_id in processed_ids
        )

        if is_duplicate:
            exception_types.append("DUPLICATE_INVOICE")

        risk_score = calculate_risk_score(
            invoice=invoice,
            vendor=vendor,
            exception_types=exception_types,
            is_duplicate=is_duplicate,
        )

        route = determine_route(
            risk_score,
            exception_types,
        )

        explanation = (
            f"Invoice {invoice.invoice_id} was routed to {route}. "
            f"Detected exceptions: "
            f"{', '.join(exception_types) if exception_types else 'none'}. "
            f"Risk score: {risk_score}."
        )

        decisions.append(
            ProcessDecision(
                invoice_id=invoice.invoice_id,
                exception_types=exception_types,
                variance_percent=variance_percent,
                risk_score=risk_score,
                route=route,
                explanation=explanation,
            )
        )

        processed_ids.add(invoice.invoice_id)

    return decisions
