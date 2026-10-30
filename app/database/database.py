from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./data/quoteguard.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_database_schema() -> None:
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    if "quotes" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("quotes")}

    with engine.begin() as connection:
        for column_name, ddl in {
            "quote_number": "VARCHAR(50) NOT NULL DEFAULT 'Q-LEGACY'",
            "project_id": "INTEGER",
            "service_type": "VARCHAR(200)",
            "project_name": "VARCHAR(200)",
            "labor_hours": "FLOAT",
            "labor_rate": "FLOAT",
            "material_cost": "FLOAT",
            "overhead_rate": "FLOAT",
            "contingency_rate": "FLOAT",
            "target_margin": "FLOAT",
            "total_cost": "FLOAT",
            "recommended_price": "FLOAT",
            "expected_profit": "FLOAT",
            "expected_margin": "FLOAT",
            "decision": "VARCHAR(50)",
            "status": "VARCHAR(50) NOT NULL DEFAULT 'draft'",
            "notes": "VARCHAR(1000)",
        }.items():
            if column_name not in existing_columns:
                connection.execute(text(f"ALTER TABLE quotes ADD COLUMN {column_name} {ddl}"))