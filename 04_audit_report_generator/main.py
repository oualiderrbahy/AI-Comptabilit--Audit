from report_generator import generate_audit_report


def main():
    controls = [
        {"name": "Vérification des écritures", "passed": True},
        {"name": "Rapprochement bancaire", "passed": False},
        {"name": "Contrôle TVA", "passed": True},
    ]
    financial_summary = {"revenue": 950000, "margin": 26.5, "risk": "modéré"}
    report = generate_audit_report(controls, financial_summary)
    print(report)


if __name__ == "__main__":
    main()
