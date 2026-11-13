from ratios import compute_ratios


def main():
    financials = {
        "revenue": 1000000,
        "cost_of_goods_sold": 600000,
        "net_income": 160000,
        "assets": 800000,
        "liabilities": 320000,
        "current_assets": 250000,
        "current_liabilities": 130000,
    }
    print(compute_ratios(financials))


if __name__ == "__main__":
    main()
