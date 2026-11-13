from __future__ import annotations

import io

import pandas as pd
import pytest

from reconciliation import (
    export_excel_report,
    load_csv,
    load_transactions,
    normalize_rows,
    reconcile,
    result_tables,
)


def test_original_csv_loader_and_matching_are_preserved():
    bank = load_csv("data/bank_statement.csv")
    ledger = load_csv("data/journal.csv")
    result = reconcile(bank, ledger, tolerance=0)
    assert len(result["matched"]) == 3
    assert len(result["unmatched_bank"]) == 2
    assert len(result["unmatched_journal"]) == 2


def test_matches_amount_within_tolerance_and_only_once():
    bank = [{"date": "2024-01-01", "amount": "100.00"}, {"date": "2024-01-01", "amount": "100.00"}]
    ledger = [{"date": "01/01/2024", "amount": "101,50"}]
    result = reconcile(bank, ledger, tolerance=2)
    assert len(result["matched"]) == 1
    assert len(result["unmatched_bank"]) == 1
    assert result["matched"][0]["journal"]["amount"] == 101.5


def test_normalizes_french_headers_and_european_amount():
    rows = normalize_rows([{"Date opération": "05/01/2024", "Montant": "1 234,50", "Libellé": "Virement"}])
    assert rows[0]["date"] == "2024-01-05"
    assert rows[0]["amount"] == 1234.5
    assert rows[0]["description"] == "Virement"


def test_missing_required_column_fails_clearly():
    with pytest.raises(ValueError, match="Colonnes obligatoires manquantes"):
        normalize_rows([{"date": "2024-01-01", "description": "sans montant"}])


def test_invalid_amount_and_date_are_reported():
    with pytest.raises(ValueError, match="montant non fini|could not convert"):
        normalize_rows([{"date": "2024-01-01", "amount": "pas un nombre"}])
    with pytest.raises(ValueError, match="date invalide"):
        normalize_rows([{"date": "nonsense", "amount": 10}])


def test_empty_input_and_invalid_tolerance_are_rejected():
    with pytest.raises(ValueError, match="aucune écriture"):
        reconcile([], [{"date": "2024-01-01", "amount": 10}])
    with pytest.raises(ValueError, match="tolérance"):
        reconcile([{"date": "2024-01-01", "amount": 10}], [{"date": "2024-01-01", "amount": 10}], -1)


def test_load_csv_from_upload_bytes():
    data = b"date,amount,description\n2024-01-01,10.00,Test\n"
    rows = load_transactions(data, "test.csv")
    assert rows[0]["amount"] == 10.0


def test_load_and_export_excel_report():
    source = io.BytesIO()
    pd.DataFrame([{"date": "2024-01-01", "amount": 12.0, "description": "Test"}]).to_excel(source, index=False)
    rows = load_transactions(source.getvalue(), "test.xlsx")
    result = reconcile(rows, rows, tolerance=0)
    report = export_excel_report(result)
    workbook = pd.ExcelFile(io.BytesIO(report))
    assert {"Synthese", "Rapprochees", "Ecarts banque", "Ecarts grand livre"}.issubset(workbook.sheet_names)


def test_result_tables_have_discrepancy_rows():
    result = reconcile(
        [{"date": "2024-01-01", "amount": 10, "description": "Banque"}],
        [{"date": "2024-01-02", "amount": 20, "description": "Livre"}],
        tolerance=0,
    )
    tables = result_tables(result)
    assert tables["rapprochees"].empty
    assert len(tables["ecarts_banque"]) == 1
    assert len(tables["ecarts_grand_livre"]) == 1
