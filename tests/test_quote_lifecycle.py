from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.main import app
from app.models.customer import Customer
from app.models.quote import Quote


client = TestClient(app)


def _clean_quotes():
    db = SessionLocal()
    try:
        db.query(Quote).delete()
        db.query(Customer).delete()
        db.commit()
    finally:
        db.close()


def test_quote_status_updates_and_summary():
    _clean_quotes()

    db = SessionLocal()
    try:
        customer = Customer(name="Acme", email="acme@example.com", company="Acme")
        db.add(customer)
        db.commit()
        db.refresh(customer)

        quote = Quote(
            customer_id=customer.id,
            service_type="Website Development",
            project_name="Landing Page",
            labor_hours=40,
            labor_rate=80,
            material_cost=1000,
            overhead_rate=0.15,
            contingency_rate=0.1,
            target_margin=0.2,
            total_cost=7000,
            recommended_price=9000,
            expected_profit=2000,
            expected_margin=0.22,
            decision="APPROVE",
            status="draft",
        )
        db.add(quote)
        db.commit()
        db.refresh(quote)
    finally:
        db.close()

    response = client.patch(f"/quotes/{quote.id}/status", json={"status": "approved", "notes": "Client accepted"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "approved"
    assert payload["notes"] == "Client accepted"

    list_response = client.get("/quotes/")
    assert list_response.status_code == 200
    quotes = list_response.json()
    assert any(item["id"] == quote.id and item["status"] == "approved" for item in quotes)

    summary_response = client.get("/reports/summary")
    assert summary_response.status_code == 200
    summary = summary_response.json()
    assert summary["total_quotes"] >= 1
    assert summary["approved_quotes"] >= 1
    assert "by_service_type" in summary
