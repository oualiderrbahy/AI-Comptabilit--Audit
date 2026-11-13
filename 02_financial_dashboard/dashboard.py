from __future__ import annotations

import csv
from pathlib import Path


def load_financial_data(csv_path: str | Path):
    with open(csv_path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def compute_kpis(rows):
    revenue = sum(float(row["revenue"]) for row in rows)
    costs = sum(float(row["costs"]) for row in rows)
    profit = revenue - costs
    margin = (profit / revenue * 100) if revenue else 0.0
    cash_balance = revenue * 0.25 + 12000
    return {
        "revenue": round(revenue, 2),
        "costs": round(costs, 2),
        "profit": round(profit, 2),
        "margin": round(margin, 2),
        "cash_balance": round(cash_balance, 2),
    }


def build_dashboard_summary(data_path: str | Path):
    rows = load_financial_data(data_path)
    return compute_kpis(rows)
