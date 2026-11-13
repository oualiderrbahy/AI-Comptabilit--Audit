from report_generator import generate_audit_report


def test_generate_audit_report():
    report = generate_audit_report(
        [{"name": "Vérification des écritures", "passed": True}],
        {"revenue": 100000, "margin": 20.0, "risk": "faible"},
    )
    assert "# Rapport d’audit" in report
    assert "Vérification des écritures" in report
    assert "20.0" in report
