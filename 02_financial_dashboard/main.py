from pathlib import Path

from dashboard import build_dashboard_summary


def main():
    base = Path(__file__).resolve().parent
    summary = build_dashboard_summary(base / "data" / "finance.csv")
    print("Tableau de bord financier")
    for key, value in summary.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
