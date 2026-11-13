from __future__ import annotations


def simulate_tax(income: float, expenses: float, vat_rate: float = 0.2):
    taxable_base = max(income - expenses, 0.0)
    tax = taxable_base * vat_rate
    return {
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "taxable_base": round(taxable_base, 2),
        "tax": round(tax, 2),
        "net_after_tax": round(income - tax, 2),
    }


def scenario_comparison(income: float, expenses: float):
    base = simulate_tax(income, expenses)
    optimistic = simulate_tax(income * 1.1, expenses * 0.95)
    pessimistic = simulate_tax(income * 0.9, expenses * 1.05)
    return {
        "base": base,
        "optimistic": optimistic,
        "pessimistic": pessimistic,
    }


try:
    from fastapi import FastAPI
except ImportError:  # pragma: no cover
    FastAPI = None

if FastAPI is not None:
    app = FastAPI(title="Tax Simulation API")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/simulate")
    def simulate_endpoint(income: float, expenses: float, vat_rate: float = 0.2):
        return simulate_tax(income, expenses, vat_rate)

    @app.get("/compare")
    def compare_endpoint(income: float, expenses: float):
        return scenario_comparison(income, expenses)
