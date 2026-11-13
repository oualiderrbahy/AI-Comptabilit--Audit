from __future__ import annotations


def compute_ratios(financials):
    revenue = float(financials["revenue"])
    net_income = float(financials["net_income"])
    assets = float(financials["assets"])
    liabilities = float(financials["liabilities"])
    current_assets = float(financials["current_assets"])
    current_liabilities = float(financials["current_liabilities"])

    return {
        "gross_margin": round(((revenue - financials["cost_of_goods_sold"]) / revenue) * 100, 2) if revenue else 0.0,
        "roa": round((net_income / assets) * 100, 2) if assets else 0.0,
        "debt_ratio": round((liabilities / assets) * 100, 2) if assets else 0.0,
        "current_ratio": round(current_assets / current_liabilities, 2) if current_liabilities else 0.0,
    }
