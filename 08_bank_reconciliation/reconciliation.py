from __future__ import annotations

import csv


def reconcile(bank_rows, journal_rows, tolerance=50.0):
    matched = []
    unmatched_bank = []
    unmatched_journal = list(journal_rows)

    for row in bank_rows:
        amount = float(row["amount"])
        date = row["date"]
        match = None
        for journal in unmatched_journal:
            if journal["date"] == date and abs(float(journal["amount"]) - amount) <= tolerance:
                match = journal
                break
        if match is not None:
            matched.append({"bank": row, "journal": match})
            unmatched_journal.remove(match)
        else:
            unmatched_bank.append(row)
    return {"matched": matched, "unmatched_bank": unmatched_bank, "unmatched_journal": unmatched_journal}


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))
