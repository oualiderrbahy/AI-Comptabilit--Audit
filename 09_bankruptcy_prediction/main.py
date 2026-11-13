from bankruptcy_model import bankruptcy_score, classify_risk


def main():
    company = {"assets": 1000000, "liabilities": 600000, "current_assets": 200000, "current_liabilities": 180000, "net_income": 50000, "revenue": 700000}
    score = bankruptcy_score(company)
    print({"score": score, "risk": classify_risk(score)})


if __name__ == "__main__":
    main()
