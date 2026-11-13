from tax_logic import simulate_tax


def test_simulate_tax():
    result = simulate_tax(150000, 45000)
    assert result["taxable_base"] == 105000.0
    assert result["tax"] == 21000.0
    assert result["net_after_tax"] == 129000.0
