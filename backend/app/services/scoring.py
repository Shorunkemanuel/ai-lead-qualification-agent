from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models import Lead, LeadScore
from app.schemas import LeadScoreInput


_WEIGHTS = {
    "icp_fit": Decimal("0.30"),
    "company_potential": Decimal("0.20"),
    "role_relevance": Decimal("0.20"),
    "buying_signal": Decimal("0.20"),
    "data_quality": Decimal("0.10"),
}


def score_tier(score: int) -> str:
    if score >= 80:
        return "HIGH"
    if score >= 60:
        return "MEDIUM"
    if score >= 40:
        return "LOW"
    return "NOT QUALIFIED"


def calculate_overall_score(factors: LeadScoreInput) -> int:
    weighted_score = sum(
        Decimal(getattr(factors, name)) * weight
        for name, weight in _WEIGHTS.items()
    )
    return int(weighted_score.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def save_score(
    session: Session, lead: Lead, factors: LeadScoreInput
) -> LeadScore:
    score = LeadScore(
        lead=lead,
        overall_score=calculate_overall_score(factors),
        **factors.model_dump(exclude={"rationale"}),
        rationale=factors.rationale,
    )
    session.add(score)
    session.commit()
    session.refresh(score)
    return score
