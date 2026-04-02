import re


class AIProcessor:

    @staticmethod
    def extract_entities(text: str):
        amount = AIProcessor._extract_amount(text)
        date = AIProcessor._extract_date(text)
        issue = AIProcessor._classify_issue(text)
        risk = AIProcessor._detect_risk(text)

        return {
            "amount": amount,
            "date": date,
            "issue_type": issue,
            "risk_level": risk
        }

    @staticmethod
    def summarize(text: str):
        sentences = text.split(".")
        return sentences[0] if sentences else text

    @staticmethod
    def _extract_amount(text: str):
        match = re.search(r"\$?\d+(?:,\d{3})*(?:\.\d{2})?", text)
        return match.group() if match else None

    @staticmethod
    def _extract_date(text: str):
        match = re.search(r"(Jan|Feb|Mar|March|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{1,2}", text)
        return match.group() if match else None

    @staticmethod
    def _classify_issue(text: str):
        text_lower = text.lower()

        if "fraud" in text_lower or "unauthorized" in text_lower:
            return "fraud"

        if "refund" in text_lower:
            return "refund"

        return "general"

    @staticmethod
    def _detect_risk(text: str):
        text_lower = text.lower()

        if "unauthorized" in text_lower or "suspicious" in text_lower:
            return "high"

        return "low"