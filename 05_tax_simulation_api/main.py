from tax_logic import scenario_comparison, simulate_tax


def main():
    result = simulate_tax(150000, 45000)
    print(result)
    print(scenario_comparison(150000, 45000))


if __name__ == "__main__":
    main()
