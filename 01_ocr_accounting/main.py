from __future__ import annotations

from pathlib import Path

from invoice_parser import load_invoices


def main():
    base = Path(__file__).resolve().parent
    invoices = load_invoices(base / "data" / "invoices.csv")
    print("Factures traitées :")
    for invoice in invoices:
        print(f"- {invoice['invoice_id']}: fournisseur={invoice['supplier']}, date={invoice['date']}, montant={invoice['amount']}, TVA={invoice['vat']}")


if __name__ == "__main__":
    main()
