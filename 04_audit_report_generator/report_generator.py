from __future__ import annotations


def generate_audit_report(control_results, financial_summary):
    lines = [
        "# Rapport d’audit",
        "",
        "## Résumé exécutif",
        f"- Revenu total : {financial_summary['revenue']} €",
        f"- Marge : {financial_summary['margin']} %",
        f"- Risque global : {financial_summary['risk']}",
        "",
        "## Contrôles effectués",
    ]
    for control in control_results:
        status = "OK" if control["passed"] else "À corriger"
        lines.append(f"- {control['name']}: {status}")
    return "\n".join(lines)
