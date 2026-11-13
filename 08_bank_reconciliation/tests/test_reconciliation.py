from reconciliation import load_csv, reconcile


def test_reconcile():
    bank_rows = load_csv("08_bank_reconciliation/data/bank_statement.csv")
    journal_rows = load_csv("08_bank_reconciliation/data/journal.csv")
    result = reconcile(bank_rows, journal_rows)
    assert len(result["matched"]) == 2
    assert len(result["unmatched_bank"]) == 0
    assert len(result["unmatched_journal"]) == 1
