from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.customer import Customer
from app.models.quote import Quote


client = TestClient(app)


def test_invalid_margin_returns_json_error():
    response = client.post(
        "/intelligence/analyze",
        json={
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "project_name": "Demo",
            "service_type": "Website Development",
            "labor_hours": 40,
            "labor_rate": 80,
            "material_cost": 1000,
            "overhead_rate": 15,
            "contingency_rate": 10,
            "target_margin": 200,
            "historical_estimation_variance": 0,
        },
    )

    assert response.status_code == 400
    payload = response.json()
    assert "Target margin" in payload["detail"]


def test_each_analysis_is_saved_for_existing_customer():
    db = SessionLocal()
    try:
        db.query(Quote).delete()
        db.query(Customer).delete()
        db.commit()
    finally:
        db.close()

    payload = {
        "customer_name": "Repeat Customer",
        "customer_email": "repeat@example.com",
        "project_name": "First Project",
        "service_type": "Website Development",
        "labor_hours": 40,
        "labor_rate": 80,
        "material_cost": 1000,
        "overhead_rate": 0.15,
        "contingency_rate": 0.10,
        "target_margin": 0.20,
        "historical_estimation_variance": 0,
    }

    first_response = client.post("/intelligence/analyze", json=payload)
    assert first_response.status_code == 200

    payload["project_name"] = "Second Project"
    second_response = client.post("/intelligence/analyze", json=payload)
    assert second_response.status_code == 200

    quotes_response = client.get("/quotes/")
    assert quotes_response.status_code == 200
    quotes = quotes_response.json()
    assert len(quotes) == 2
    assert {quote["project_name"] for quote in quotes} == {
        "First Project",
        "Second Project",
    }
