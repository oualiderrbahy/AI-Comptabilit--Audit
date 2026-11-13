from dashboard import build_dashboard_summary


def test_dashboard_summary():
    summary = build_dashboard_summary("02_financial_dashboard/data/finance.csv")
    assert summary["revenue"] == 930000.0
    assert summary["profit"] == 270000.0
    assert summary["margin"] == 29.03
    assert summary["cash_balance"] == 232500.0
