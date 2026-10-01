import os
import tempfile
import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.database import initialize_database
from app.models import Base, Lead, LeadScore


class DatabaseTests(unittest.TestCase):
    def test_lead_and_score_persist_with_relationship(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "leads.db")
            engine = create_engine(f"sqlite:///{database_path}")
            initialize_database(bind=engine)

            with Session(engine) as session:
                lead = Lead(name="Avery Chen", company="Example Co")
                lead.scores.append(
                    LeadScore(
                        icp_fit=80,
                        company_potential=70,
                        role_relevance=90,
                        buying_signal=50,
                        data_quality=100,
                        overall_score=77,
                        rationale="Strong role fit",
                    )
                )
                session.add(lead)
                session.commit()
                lead_id = lead.id

            with Session(engine) as session:
                saved_lead = session.scalar(select(Lead).where(Lead.id == lead_id))
                self.assertEqual(saved_lead.name, "Avery Chen")
                self.assertEqual(len(saved_lead.scores), 1)
                self.assertEqual(saved_lead.scores[0].overall_score, 77)

            engine.dispose()
