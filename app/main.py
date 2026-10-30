from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database.database import engine
from app.database.database import Base, ensure_database_schema

from app.models.customer import Customer
from app.models.job import Job
from app.models.quote import Quote
from app.models.material import Material

from app.models.job_cost import JobCost
from app.models.quote_risk import QuoteRisk

from app.api.customers import router as customers_router
from app.api.projects import router as projects_router
from app.api.pricing import router as pricing_router
from app.api.intelligence import router as intelligence_router
from app.api.quotes import router as quotes_router
from app.api.reports import router as reports_router


ensure_database_schema()


app = FastAPI(
    title="QuoteGuard",
    description=(
        "AI-powered quoting intelligence "
        "for small and medium-sized businesses."
    ),
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


app.include_router(
    customers_router
)

app.include_router(
    projects_router
)

app.include_router(
    pricing_router
)

app.include_router(
    intelligence_router
)

app.include_router(
    quotes_router
)

app.include_router(
    reports_router
)


@app.get("/")
def root():

    return {
        "application": "QuoteGuard",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/app")
def application():

    return FileResponse(
        "static/index.html"
    )


@app.get("/dashboard")
def dashboard_page():

    return FileResponse(
        "static/dashboard.html"
    )


@app.get("/customer")
def customer_page():

    return FileResponse(
        "static/customer.html"
    )