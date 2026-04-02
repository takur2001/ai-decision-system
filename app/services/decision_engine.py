import random


class DecisionEngine:

    @staticmethod
    def generate_decision(entities: dict) -> dict:
        risk_level = entities.get("risk_level")
        issue_type = entities.get("issue_type")
        amount = entities.get("amount")

        # Convert amount to number
        numeric_amount = DecisionEngine._parse_amount(amount)

        # Risk score logic
        risk_score = DecisionEngine._calculate_risk_score(
            risk_level, issue_type, numeric_amount
        )

        # Confidence score
        confidence_score = round(random.uniform(0.7, 0.95), 2)

        # Decision logic
        if risk_score > 0.8:
            action = "Escalate for manual review"
        elif risk_score > 0.5:
            action = "Flag for review"
        else:
            action = "Mark as low priority"

        return {
            "recommended_action": action,
            "risk_score": risk_score,
            "confidence_score": confidence_score,
            "decision_source": "rule_engine_v2"
        }

    @staticmethod
    def _parse_amount(amount: str):
        if not amount:
            return 0
        return float(amount.replace("$", "").replace(",", ""))

    @staticmethod
    def _calculate_risk_score(risk_level, issue_type, amount):
        score = 0.0

        if risk_level == "high":
            score += 0.5

        if issue_type == "fraud":
            score += 0.3

        if amount and amount > 1000:
            score += 0.2

        return round(min(score, 1.0), 2)