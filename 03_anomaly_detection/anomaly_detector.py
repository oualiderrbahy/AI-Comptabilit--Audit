from __future__ import annotations

import csv
from pathlib import Path


def load_transactions(csv_path: str | Path):
    with open(csv_path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def detect_anomalies(rows, threshold=2.5):
    amounts = [float(row["amount"]) for row in rows]
    mean_amount = sum(amounts) / len(amounts)
    variance = sum((amount - mean_amount) ** 2 for amount in amounts) / len(amounts)
    std_dev = variance ** 0.5

    anomalies = []
    for row in rows:
        amount = float(row["amount"])
        z_score = abs((amount - mean_amount) / std_dev) if std_dev else 0.0
        if z_score > threshold:
            anomalies.append({
                "id": row["id"],
                "account": row["account"],
                "amount": amount,
                "z_score": round(z_score, 2),
                "risk": "high",
            })
    return anomalies
