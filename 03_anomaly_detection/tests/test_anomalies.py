from anomaly_detector import detect_anomalies, load_transactions


def test_detect_anomalies():
    rows = load_transactions("03_anomaly_detection/data/transactions.csv")
    anomalies = detect_anomalies(rows)
    assert len(anomalies) >= 1
    assert anomalies[0]["account"] == "607000"
    assert anomalies[0]["risk"] == "high"
