import unittest

from pydantic import ValidationError

from app.schemas import LeadScoreInput
from app.services.scoring import calculate_overall_score, score_tier


class ScoringTests(unittest.TestCase):
    def test_weighted_score_uses_specified_factors(self):
        factors = LeadScoreInput(
            icp_fit=80,
            company_potential=70,
            role_relevance=90,
            buying_signal=50,
            data_quality=100,
        )

        self.assertEqual(calculate_overall_score(factors), 76)

    def test_score_tiers_match_specification_boundaries(self):
        self.assertEqual(score_tier(80), "HIGH")
        self.assertEqual(score_tier(60), "MEDIUM")
        self.assertEqual(score_tier(40), "LOW")
        self.assertEqual(score_tier(39), "NOT QUALIFIED")

    def test_score_factors_must_be_within_zero_and_one_hundred(self):
        with self.assertRaises(ValidationError):
            LeadScoreInput(
                icp_fit=101,
                company_potential=0,
                role_relevance=0,
                buying_signal=0,
                data_quality=0,
            )
