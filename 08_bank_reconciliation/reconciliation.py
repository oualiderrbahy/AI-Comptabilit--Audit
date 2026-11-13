from __future__ import annotations

import csv
import io
import math
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd


REQUIRED_COLUMNS = {"date", "amount"}
COLUMN_ALIASES = {
    "date": {"date", " 날짜", "jour", "date operation", "date d'operation", "date opération", "date comptable"},
    "amount": {"amount", "montant", "montant eur", "montant (€)", "debit credit", "valeur"},
    "description": {"description", "libelle", "libellé", "transaction", "motif", "intitule", "intitulé"},
    "reference": {"reference", "référence", "ref", "numero", "numéro", "piece", "pièce"},
    "account": {"account", "compte", "compte general", "compte général", "account number"},
}


def _column_key(value: Any) -> str:
    return " ".join(str(value).strip().lower().replace("_", " ").split())


def _parse_amount(value: Any) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        raise ValueError("montant manquant")
    if isinstance(value, (int, float)):
        amount = float(value)
    else:
        text = str(value).strip().replace("€", "").replace("\u00a0", "").replace(" ", "")
        if not text:
            raise ValueError("montant manquant")
        # Le séparateur le plus à droite est interprété comme séparateur décimal.
        if "," in text and "." in text:
            decimal = "," if text.rfind(",") > text.rfind(".") else "."
            thousands = "." if decimal == "," else ","
            text = text.replace(thousands, "").replace(decimal, ".")
        elif "," in text:
            text = text.replace(",", ".")
        amount = float(text)
    if not math.isfinite(amount):
        raise ValueError("montant non fini")
    return amount


def _parse_date(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        raise ValueError("date manquante")
    if isinstance(value, (date, datetime, pd.Timestamp)):
        parsed = pd.Timestamp(value)
    else:
        text = str(value).strip()
        if not text:
            raise ValueError("date manquante")
        parsed = pd.to_datetime(text, errors="coerce", dayfirst=True)
    if pd.isna(parsed):
        raise ValueError(f"date invalide : {value}")
    return parsed.strftime("%Y-%m-%d")


def normalize_rows(rows: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Normalize common French/English column names and validate transaction rows."""
    normalized: list[dict[str, Any]] = []
    for index, original in enumerate(rows, start=1):
        if not isinstance(original, Mapping):
            raise ValueError(f"Ligne {index} : format de ligne invalide.")
        row = dict(original)
        lookup = {_column_key(key): value for key, value in row.items()}
        mapped: dict[str, Any] = {}
        for canonical, aliases in COLUMN_ALIASES.items():
            for key, value in lookup.items():
                if key in aliases or key == canonical:
                    mapped[canonical] = value
                    break
        missing = REQUIRED_COLUMNS - mapped.keys()
        if missing:
            raise ValueError("Colonnes obligatoires manquantes : " + ", ".join(sorted(missing)))
        try:
            mapped["date"] = _parse_date(mapped["date"])
            mapped["amount"] = _parse_amount(mapped["amount"])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Ligne {index} : {exc}") from exc
        mapped["description"] = str(mapped.get("description") or "").strip()
        # Preserve source fields not covered by standard columns.
        for key, value in row.items():
            if key not in mapped:
                mapped[key] = value
        normalized.append(mapped)
    if not normalized:
        raise ValueError("Le fichier ne contient aucune écriture exploitable.")
    return normalized


def load_transactions(file_or_path: Any, filename: str | None = None) -> list[dict[str, Any]]:
    """Read and validate a CSV or Excel file/path/Streamlit UploadedFile."""
    if isinstance(file_or_path, (str, Path)):
        path = Path(file_or_path)
        name = filename or path.name
        payload: Any = path
    else:
        name = filename or getattr(file_or_path, "name", "")
        payload = file_or_path.getvalue() if hasattr(file_or_path, "getvalue") else file_or_path
    suffix = Path(name).suffix.lower()
    try:
        if isinstance(payload, Path):
            frame = pd.read_csv(payload) if suffix == ".csv" else pd.read_excel(payload)
        else:
            content = payload if isinstance(payload, bytes) else bytes(payload)
            if suffix == ".csv":
                try:
                    frame = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")
                except UnicodeDecodeError:
                    frame = pd.read_csv(io.BytesIO(content), encoding="cp1252")
            elif suffix in {".xlsx", ".xls"}:
                frame = pd.read_excel(io.BytesIO(content))
            else:
                raise ValueError("Format non pris en charge. Utilisez un fichier CSV ou Excel (.xlsx, .xls).")
    except (ValueError, OSError, pd.errors.ParserError, ImportError) as exc:
        if isinstance(exc, ValueError) and str(exc).startswith("Format non pris en charge"):
            raise
        raise ValueError(f"Impossible de lire le fichier : {exc}") from exc
    if frame.empty:
        raise ValueError("Le fichier est vide.")
    # Header matching is case/whitespace insensitive; normalize_rows reports missing columns clearly.
    return normalize_rows(frame.to_dict(orient="records"))


def load_csv(path):
    """Backward-compatible CSV loader retained for the original command-line project."""
    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def reconcile(bank_rows, journal_rows, tolerance=50.0):
    """Match one ledger entry per bank line on date and amount within tolerance.

    This retains the original result shape and matching semantics, while safely
    accepting normalized records as well as the project's original CSV rows.
    """
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError) as exc:
        raise ValueError("La tolérance doit être un nombre positif ou nul.") from exc
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("La tolérance doit être un nombre positif ou nul.")

    bank = normalize_rows(bank_rows)
    journal = normalize_rows(journal_rows)
    matched = []
    unmatched_bank = []
    unmatched_journal = list(journal)

    for row in bank:
        match_index = next((index for index, entry in enumerate(unmatched_journal)
                            if entry["date"] == row["date"]
                            and abs(entry["amount"] - row["amount"]) <= tolerance), None)
        if match_index is None:
            unmatched_bank.append(row)
        else:
            match = unmatched_journal.pop(match_index)
            matched.append({"bank": row, "journal": match})
    return {"matched": matched, "unmatched_bank": unmatched_bank, "unmatched_journal": unmatched_journal}


def result_tables(result: Mapping[str, Any]) -> dict[str, pd.DataFrame]:
    matched = [
        {"Date": pair["bank"]["date"], "Montant banque (€)": pair["bank"]["amount"],
         "Montant grand livre (€)": pair["journal"]["amount"],
         "Écart (€)": round(pair["bank"]["amount"] - pair["journal"]["amount"], 2),
         "Libellé banque": pair["bank"].get("description", ""),
         "Libellé grand livre": pair["journal"].get("description", "")}
        for pair in result["matched"]
    ]
    def discrepancy(rows: list[dict[str, Any]], source: str) -> pd.DataFrame:
        return pd.DataFrame([{"Date": row["date"], "Montant (€)": row["amount"],
                              "Libellé": row.get("description", ""), "Origine": source}
                             for row in rows])
    return {
        "rapprochees": pd.DataFrame(matched, columns=["Date", "Montant banque (€)", "Montant grand livre (€)", "Écart (€)", "Libellé banque", "Libellé grand livre"]),
        "ecarts_banque": discrepancy(result["unmatched_bank"], "Relevé bancaire"),
        "ecarts_grand_livre": discrepancy(result["unmatched_journal"], "Grand livre"),
    }


def export_excel_report(result: Mapping[str, Any], output: Any | None = None) -> bytes:
    """Build a multi-sheet Excel report and return its bytes (or also write to output)."""
    tables = result_tables(result)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for sheet_name, key in [("Rapprochees", "rapprochees"), ("Ecarts banque", "ecarts_banque"), ("Ecarts grand livre", "ecarts_grand_livre")]:
            tables[key].to_excel(writer, sheet_name=sheet_name, index=False)
        summary = pd.DataFrame([
            {"Indicateur": "Écritures rapprochées", "Valeur": len(result["matched"])},
            {"Indicateur": "Écarts relevé bancaire", "Valeur": len(result["unmatched_bank"])},
            {"Indicateur": "Écarts grand livre", "Valeur": len(result["unmatched_journal"])},
        ])
        summary.to_excel(writer, sheet_name="Synthese", index=False)
    content = buffer.getvalue()
    if output is not None:
        output.write(content)
    return content


# Legacy public alias for callers expecting a filename-based CSV loader.
load_file = load_transactions
