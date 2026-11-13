from business_plan import build_business_plan, generate_plan_markdown


def main():
    inputs = {"monthly_revenue": 50000, "direct_cost_ratio": 0.45, "operating_cost_ratio": 0.20}
    plan = build_business_plan(inputs)
    print(generate_plan_markdown(plan))


if __name__ == "__main__":
    main()
