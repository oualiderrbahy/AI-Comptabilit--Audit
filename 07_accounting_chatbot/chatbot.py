from __future__ import annotations


KNOWLEDGE = {
    "tva": "La TVA standard est généralement de 20 % en France pour les ventes de biens et services concernés.",
    "amortissement": "L’amortissement répartit le coût d’un bien sur sa durée d’usage.",
    "bilan": "Un bilan permet de voir les actifs, passifs et capitaux propres d’une entreprise.",
    "tresorerie": "La trésorerie correspond au solde de liquidités immédiatement disponibles.",
}


def answer_question(question: str) -> str:
    normalized = question.lower()
    for key, answer in KNOWLEDGE.items():
        if key in normalized:
            return answer
    return "Je n’ai pas trouvé d’information spécifique dans ma base de connaissances. Essayez : TVA, amortissement, bilan ou trésorerie."
