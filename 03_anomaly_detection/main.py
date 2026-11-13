from pathlib import Path

from anomaly_detector import detect_anomalies, load_transactions


def main():
    base = Path(__file__).resolve().parent
    rows = load_transactions(base / "data" / "transactions.csv")
    anomalies = detect_anomalies(rows)
    print("Anomalies détectées :")
    for anomaly in anomalies:
        print(anomaly)


if __name__ == "__main__":
    main()
