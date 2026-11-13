from __future__ import annotations


def bankruptcy_score(financials):
    debt_ratio = float(financials["liabilities"]) / float(financials["assets"]) if float(financials["assets"]) else 0.0
    liquidity_ratio = float(financials["current_assets"]) / float(financials["current_liabilities"]) if float(financials["current_liabilities"]) else 0.0
    profitability_ratio = float(financials["net_income"]) / float(financials["revenue"]) if float(financials["revenue"]) else 0.0

    score = (debt_ratio * 0.5) + ((1 / liquidity_ratio) * 0.25 if liquidity_ratio else 0.25) + ((-profitability_ratio) * 0.25 if profitability_ratio else 0.0)
    return round(max(0.0, min(score, 1.0)), 3)


def classify_risk(score):
    if score >= 0.65:
        return "Élevé"
    if score >= 0.4:
        return "Moyen"
    return "Faible"
