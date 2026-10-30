from app.database.database import Base, engine, ensure_database_schema


def initialize_database():
    ensure_database_schema()
    print("QuoteGuard database initialized successfully.")


if __name__ == "__main__":
    initialize_database()