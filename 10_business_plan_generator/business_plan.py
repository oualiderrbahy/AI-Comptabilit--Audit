from __future__ import annotations


def build_business_plan(inputs):
    revenue = float(inputs["monthly_revenue"]) * 12
    direct_costs = revenue * float(inputs["direct_cost_ratio"])
    operating_costs = revenue * float(inputs["operating_cost_ratio"])
    net_profit = revenue - direct_costs - operating_costs
    return {
        "revenue": round(revenue, 2),
        "direct_costs": round(direct_costs, 2),
        "operating_costs": round(operating_costs, 2),
        "net_profit": round(net_profit, 2),
        "scenarios": {
            "optimistic": round(net_profit * 1.2, 2),
            "pessimistic": round(net_profit * 0.8, 2),
        },
    }


def generate_plan_markdown(plan):
    return f"""# Business Plan\n\n## Résultat annuel\n- Revenus : {plan['revenue']} €\n- Coûts directs : {plan['direct_costs']} €\n- Coûts opérationnels : {plan['operating_costs']} €\n- Bénéfice net : {plan['net_profit']} €\n\n## Scénarios\n- Optimiste : {plan['scenarios']['optimistic']} €\n- Pessimiste : {plan['scenarios']['pessimistic']} €\n"""
