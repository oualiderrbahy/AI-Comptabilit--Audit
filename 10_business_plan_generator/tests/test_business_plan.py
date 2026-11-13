from business_plan import build_business_plan, generate_plan_markdown


def test_business_plan_generation():
    plan = build_business_plan({"monthly_revenue": 50000, "direct_cost_ratio": 0.45, "operating_cost_ratio": 0.20})
    assert plan["revenue"] == 600000.0
    assert plan["net_profit"] == 210000.0
    assert plan["scenarios"]["optimistic"] == 252000.0
    assert "Business Plan" in generate_plan_markdown(plan)
