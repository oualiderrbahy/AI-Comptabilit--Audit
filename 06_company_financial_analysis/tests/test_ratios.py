from ratios import compute_ratios


def test_compute_ratios():
    financials = {
        "revenue": 1000000,
        "cost_of_goods_sold": 600000,
        "net_income": 160000,
        "assets": 800000,
        "liabilities": 320000,
        "current_assets": 250000,
        "current_liabilities": 130000,
    }
    ratios = compute_ratios(financials)
    assert ratios["gross_margin"] == 40.0
    assert ratios["roa"] == 20.0
    assert ratios["debt_ratio"] == 40.0
    assert ratios["current_ratio"] == 1.92
