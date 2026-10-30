from app.database.database import Base, engine

from app.models.customer import Customer
from app.models.job import Job
from app.models.quote import Quote
from app.models.material import Material
from app.models.labor import LaborRate
from app.models.job_cost import JobCost
from app.models.quote_risk import QuoteRisk


def init_database():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_database()
    print("QuoteGuard database initialized successfully.")