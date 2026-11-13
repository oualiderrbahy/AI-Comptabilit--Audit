from invoice_parser import extract_invoice_fields


def test_extract_invoice_fields_success():
    text = "Date: 2024-03-15 | Fournisseur: Boulanger | Montant total: 245.00 | TVA: 49.00"
    result = extract_invoice_fields(text)
    assert result["supplier"] == "Boulanger"
    assert result["date"] == "2024-03-15"
    assert result["amount"] == 245.0
    assert result["vat"] == 49.0


def test_extract_invoice_fields_handles_supplier_alias():
    text = "Date: 2024/04/10 | Supplier: Orange | Total: 89.90 | VAT: 17.98"
    result = extract_invoice_fields(text)
    assert result["supplier"] == "Orange"
    assert result["amount"] == 89.9
    assert result["vat"] == 17.98
