import unittest

from fastapi.testclient import TestClient
from sqlalchemy import delete, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base, Lead, LeadScore


class LeadAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(cls.engine)

        def override_database():
            with Session(cls.engine) as session:
                yield session

        app.dependency_overrides[get_db] = override_database
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        app.dependency_overrides.clear()
        cls.engine.dispose()

    def setUp(self):
        with Session(self.engine) as session:
            session.execute(delete(LeadScore))
            session.execute(delete(Lead))
            session.commit()

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_create_read_update_and_delete_lead(self):
        created = self.client.post(
            "/api/leads",
            json={"name": "  Avery Chen  ", "email": " Avery@Example.com "},
        )
        self.assertEqual(created.status_code, 201)
        lead_id = created.json()["id"]
        self.assertEqual(created.json()["name"], "Avery Chen")
        self.assertEqual(created.json()["email"], "avery@example.com")

        fetched = self.client.get(f"/api/leads/{lead_id}")
        self.assertEqual(fetched.status_code, 200)
        updated = self.client.patch(
            f"/api/leads/{lead_id}", json={"company": " Example Co "}
        )
        self.assertEqual(updated.json()["company"], "Example Co")
        self.assertEqual(self.client.delete(f"/api/leads/{lead_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/leads/{lead_id}").status_code, 404)

    def test_lead_validation_and_missing_lead_errors(self):
        invalid = self.client.post(
            "/api/leads", json={"name": "Avery", "email": "not-an-email"}
        )
        self.assertEqual(invalid.status_code, 422)
        self.assertEqual(
            self.client.post(
                "/api/leads/999/score",
                json={
                    "icp_fit": 50,
                    "company_potential": 50,
                    "role_relevance": 50,
                    "buying_signal": 50,
                    "data_quality": 50,
                },
            ).status_code,
            404,
        )

    def test_csv_import_normalizes_values_and_rejects_invalid_file_atomically(self):
        csv_bytes = (
            b"Name,Company,Email,Company Size\n"
            b"Jordan Lee,Example Inc,Jordan@Example.com,50-100\n"
        )
        imported = self.client.post(
            "/api/leads/import",
            files={"file": ("leads.csv", csv_bytes, "text/csv")},
        )
        self.assertEqual(imported.status_code, 201)
        self.assertEqual(imported.json()["imported_count"], 1)
        lead = self.client.get(f"/api/leads/{imported.json()['lead_ids'][0]}").json()
        self.assertEqual(lead["email"], "jordan@example.com")
        self.assertEqual(lead["company_size"], "50-100")

        invalid_csv = (
            b"name,email\nValid Person,valid@example.com\n"
            b"Invalid Person,not-an-email\n"
        )
        rejected = self.client.post(
            "/api/leads/import",
            files={"file": ("invalid.csv", invalid_csv, "text/csv")},
        )
        self.assertEqual(rejected.status_code, 422)
        self.assertEqual(len(self.client.get("/api/leads").json()), 1)

    def test_list_filters_and_score_persistence(self):
        lead_id = self.client.post(
            "/api/leads", json={"name": "Taylor Park", "company": "Acme"}
        ).json()["id"]
        self.client.post("/api/leads", json={"name": "Riley Jones", "company": "Elsewhere"})

        filtered = self.client.get("/api/leads", params={"company": "acme"})
        self.assertEqual(len(filtered.json()), 1)

        response = self.client.post(
            f"/api/leads/{lead_id}/score",
            json={
                "icp_fit": 80,
                "company_potential": 70,
                "role_relevance": 90,
                "buying_signal": 50,
                "data_quality": 100,
                "rationale": "Test score",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["overall_score"], 76)
        self.assertEqual(response.json()["tier"], "MEDIUM")
        detail = self.client.get(f"/api/leads/{lead_id}").json()
        self.assertEqual(len(detail["scores"]), 1)

        invalid_score = self.client.post(
            f"/api/leads/{lead_id}/score",
            json={
                "icp_fit": 101,
                "company_potential": 50,
                "role_relevance": 50,
                "buying_signal": 50,
                "data_quality": 50,
            },
        )
        self.assertEqual(invalid_score.status_code, 422)
