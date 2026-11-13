# Rapprochement bancaire intelligent

Application web Streamlit en français pour rapprocher un relevé bancaire avec un grand livre, examiner les correspondances et les écarts, puis exporter un rapport Excel.

## Fonctionnalités

- Import d’un relevé et d’un grand livre en CSV, XLSX ou XLS.
- Reconnaissance des noms de colonnes français et anglais courants (date, montant, libellé/description, compte, référence).
- Normalisation et validation des dates et montants, avec messages d’erreur explicites.
- Rapprochement un-à-un sur la date et un montant dans la tolérance définie.
- Tableaux distincts pour les écritures rapprochées, les écarts bancaires et les écarts du grand livre.
- Export Excel avec feuilles de synthèse et de détail.
- Mode de démonstration basé sur les fichiers fictifs du dossier `data/`.

## Installation et lancement

Python 3.10 ou plus récent est recommandé.

```bash
cd 08_bank_reconciliation
python -m venv .venv
# Windows : .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La démonstration est sélectionnée par défaut. Pour vos propres fichiers, choisissez **Importer mes fichiers** dans la barre latérale. Les fichiers doivent contenir au minimum une colonne de date et une colonne de montant. Les dates sont comparées après normalisation au jour près.

## Tests

Depuis le dossier du projet :

```bash
pytest -q
```

## Utilisation autonome

La fonction `reconcile(bank_rows, journal_rows, tolerance=50.0)` et le chargeur CSV `load_csv(path)` restent disponibles pour préserver l’utilisation existante. Les nouvelles fonctions de lecture, tableaux et export sont dans `reconciliation.py`.

## Limites et précautions

Cet outil est un prototype pédagogique : la tolérance ne s’applique qu’aux montants, les dates doivent correspondre au même jour, et les rapprochements sont gloutons (première correspondance disponible). Les données doivent être vérifiées avant toute écriture comptable. Ne téléversez pas de données confidentielles dans un environnement non approuvé. Les résultats ne constituent pas une validation comptable ou un avis professionnel.
