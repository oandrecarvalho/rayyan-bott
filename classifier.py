# classifier.py
from config import KEYWORDS_BY_CATEGORY

class ArticleClassifier:
    @staticmethod
    def classify(text: str) -> tuple[str, str, dict]:
        """
        Analisa o texto fornecido e retorna a decisão, o motivo e os matches.
        Regra: Se contiver pelo menos uma palavra-chave -> INCLUDE.
        """
        text_lower = text.lower()
        matches_found = {}
        total_matches = 0

        for category, terms in KEYWORDS_BY_CATEGORY.items():
            found_in_category = [term for term in terms if term in text_lower]
            if found_in_category:
                matches_found[category] = found_in_category
                total_matches += len(found_in_category)

        if total_matches > 0:
            decision = "INCLUDE"
            reason = f"Termos encontrados em: {', '.join(matches_found.keys())}."
        else:
            decision = "EXCLUDE"
            reason = "Nenhum termo correspondente encontrado no Scopus/Rayyan."

        return decision, reason, matches_found