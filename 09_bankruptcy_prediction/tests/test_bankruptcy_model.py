from bankruptcy_model import bankruptcy_score, classify_risk


def test_bankruptcy_risk():
    company = {"assets": 1000000, "liabilities": 600000, "current_assets": 200000, "current_liabilities": 180000, "net_income": 50000, "revenue": 700000}
    score = bankruptcy_score(company)
    assert score > 0
    assert classify_risk(score) in {"Faible", "Moyen", "Élevé"}
