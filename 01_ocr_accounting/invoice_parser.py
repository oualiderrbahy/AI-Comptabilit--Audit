from __future__ import annotations

import csv
import re
from pathlib import Path


def extract_invoice_fields(raw_text: str) -> dict:
    text = raw_text.replace("\n", " ")
    supplier_match = re.search(r"(?:fournisseur|supplier)\s*[:\-]?\s*([A-Z][A-Za-z0-9 &.'-]+)", text, flags=re.I)
    date_match = re.search(r"(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})", text)
    amount_match = re.search(r"(?:total|montant|ttc|amount)\s*[:\-]?\s*(\d+[\.,]\d{2})", text, flags=re.I)
    vat_match = re.search(r"(?:TVA|vat)\s*[:\-]?\s*(\d+[\.,]\d{2})", text, flags=re.I)

    supplier = supplier_match.group(1).strip() if supplier_match else "Non identifié"
    date = date_match.group(1) if date_match else "Non détectée"
    amount = float(amount_match.group(1).replace(",", ".")) if amount_match else 0.0
    vat = float(vat_match.group(1).replace(",", ".")) if vat_match else round(amount * 0.2, 2)

    return {
        "supplier": supplier,
        "date": date,
        "amount": round(amount, 2),
        "vat": round(vat, 2),
        "net_amount": round(amount - vat, 2),
    }


def load_invoices(csv_path: str | Path):
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            extracted = extract_invoice_fields(row["raw_text"])
            extracted["invoice_id"] = row["invoice_id"]
            rows.append(extracted)
    return rows


def main():
    base = Path(__file__).resolve().parent
    data_path = base / "data" / "invoices.csv"
    invoices = load_invoices(data_path)
    for invoice in invoices:
        print(invoice)


if __name__ == "__main__":
    main()
