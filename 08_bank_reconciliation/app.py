from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from reconciliation import export_excel_report, load_transactions, reconcile, result_tables

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(page_title="Rapprochement bancaire", page_icon="🏦", layout="wide")
st.markdown("""
<style>
    .main {background-color: #f5f7fb;}
    [data-testid="stMetric"] {background: white; padding: 18px; border-radius: 12px; border: 1px solid #e8edf5;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🏦 Rapprochement bancaire intelligent")
st.caption("Outil de contrôle comptable et d’audit · Importez vos fichiers, identifiez les écarts et exportez votre rapport.")

with st.sidebar:
    st.header("Paramètres")
    source = st.radio("Source des données", ["Données de démonstration", "Importer mes fichiers"], index=0)
    tolerance = st.number_input("Tolérance de rapprochement (€)", min_value=0.0, value=0.0, step=1.0,
                                help="Écart maximal accepté entre deux montants à la même date.")
    if source == "Importer mes fichiers":
        bank_file = st.file_uploader("Relevé bancaire (CSV ou Excel)", type=["csv", "xlsx", "xls"], key="bank")
        ledger_file = st.file_uploader("Grand livre (CSV ou Excel)", type=["csv", "xlsx", "xls"], key="ledger")
    else:
        bank_file = ledger_file = None
        st.info("La démonstration inclut des correspondances et des écarts volontaires.")

run_reconciliation = st.button("Lancer le rapprochement", type="primary", use_container_width=True)
if run_reconciliation:
    try:
        if source == "Données de démonstration":
            bank_rows = load_transactions(BASE_DIR / "data" / "bank_statement.csv")
            ledger_rows = load_transactions(BASE_DIR / "data" / "journal.csv")
        else:
            if bank_file is None or ledger_file is None:
                st.error("Veuillez importer les deux fichiers : le relevé bancaire et le grand livre.")
                st.stop()
            bank_rows = load_transactions(bank_file, bank_file.name)
            ledger_rows = load_transactions(ledger_file, ledger_file.name)

        result = reconcile(bank_rows, ledger_rows, tolerance=tolerance)
        st.session_state["reconciliation_result"] = result
        st.session_state["reconciliation_tables"] = result_tables(result)
        st.success("Rapprochement effectué avec succès.")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        st.error(f"Impossible d’effectuer le rapprochement : {exc}")

result = st.session_state.get("reconciliation_result")
if result:
    tables = st.session_state["reconciliation_tables"]
    total_matched = sum(pair["bank"]["amount"] for pair in result["matched"])
    left, middle, right, last = st.columns(4)
    left.metric("Écritures rapprochées", len(result["matched"]))
    middle.metric("Montant rapproché", f"{total_matched:,.2f} €".replace(",", " "))
    right.metric("Écarts banque", len(result["unmatched_bank"]))
    last.metric("Écarts grand livre", len(result["unmatched_journal"]))

    st.subheader("Écritures rapprochées")
    if tables["rapprochees"].empty:
        st.info("Aucune écriture rapprochée pour les paramètres sélectionnés.")
    else:
        st.dataframe(tables["rapprochees"], use_container_width=True, hide_index=True)

    left_tab, right_tab = st.columns(2)
    with left_tab:
        st.subheader("Écarts du relevé bancaire")
        if tables["ecarts_banque"].empty:
            st.success("Aucun écart sur le relevé bancaire.")
        else:
            st.dataframe(tables["ecarts_banque"], use_container_width=True, hide_index=True)
    with right_tab:
        st.subheader("Écarts du grand livre")
        if tables["ecarts_grand_livre"].empty:
            st.success("Aucun écart dans le grand livre.")
        else:
            st.dataframe(tables["ecarts_grand_livre"], use_container_width=True, hide_index=True)

    try:
        report_bytes = export_excel_report(result)
        st.download_button("⬇️ Télécharger le rapport Excel", data=report_bytes,
                           file_name="rapport_rapprochement_bancaire.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           type="primary")
    except (ValueError, OSError, ImportError) as exc:
        st.error(f"La création du rapport Excel a échoué : {exc}")
else:
    st.info("Choisissez la démonstration ou importez vos fichiers, puis lancez le rapprochement.")
    st.markdown("**Format attendu :** colonnes date et montant obligatoires. Les colonnes libellé/description, référence et compte sont facultatives. Les noms français et anglais usuels sont reconnus.")
