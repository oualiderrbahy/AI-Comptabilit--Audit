from pathlib import Path

from reconciliation import load_csv, reconcile


def main():
    base = Path(__file__).resolve().parent
    bank_rows = load_csv(base / "data" / "bank_statement.csv")
    journal_rows = load_csv(base / "data" / "journal.csv")
    result = reconcile(bank_rows, journal_rows)
    print(result)


if __name__ == "__main__":
    main()
