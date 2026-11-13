# OCR comptable

Application de démonstration pour extraire automatiquement les informations clés d’une facture à partir de texte brut.

## Fonctionnement

Le projet lit des factures fictives au format CSV, extrait automatiquement :
- date
- fournisseur
- montant total
- TVA
- montant net

## Démarrage

```bash
cd 01_ocr_accounting
pip install -r requirements.txt
python main.py
pytest -q
```
