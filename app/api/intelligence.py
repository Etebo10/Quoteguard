from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.models.project import Project
from app.models.quote import Quote

from app.schemas.intelligence import (
    QuoteIntelligenceRequest,
    QuoteIntelligenceResponse,
)

from app.services.pricing_engine import (
    PricingInput,
    calculate_quote,
)

from app.rules.risk_engine import (
    analyze_quote_risks,
)

from app.services.ai_analyst import (
    analyze_quote_with_ai,
)
from app.services.project_intelligence import build_historical_evidence

router = APIRouter(
    prefix="/intelligence",
    tags=["Quote Intelligence"],
)


@router.post(
    "/analyze",
)
def analyze_quote(
    request: QuoteIntelligenceRequest,
    db: Session = Depends(get_db),
):
    try:
        pricing_input = PricingInput(
            labor_hours=request.labor_hours,
            labor_rate=request.labor_rate,
            material_cost=request.material_cost,
            overhead_rate=request.overhead_rate,
            contingency_rate=request.contingency_rate,
            target_margin=request.target_margin,
        )

        pricing = calculate_quote(
            pricing_input
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


    historical_projects = (
        db.query(Project)
        .filter(Project.status == "completed")
        .filter(Project.service_type == request.service_type)
        .all()
    )

    historical_evidence = build_historical_evidence(
        [
            {
                "service_type": project.service_type,
                "status": project.status,
                "customer_id": project.customer_id,
                "estimated_labor_hours": project.estimated_labor_hours,
                "actual_labor_hours": project.actual_labor_hours,
                "estimated_material_cost": project.estimated_material_cost,
                "actual_material_cost": project.actual_material_cost,
                "quoted_price": project.quoted_price,
                "final_price": project.final_price,
            }
            for project in historical_projects
        ],
        service_type=request.service_type,
    )

    risks = analyze_quote_risks(
        expected_margin=pricing.expected_margin,

        estimation_variance=(
            request.historical_estimation_variance
        ),
    )


    quote_data = {

        "pricing": {

            "labor_cost":
                pricing.labor_cost,

            "material_cost":
                pricing.material_cost,

            "base_cost":
                pricing.base_cost,

            "overhead_cost":
                pricing.overhead_cost,

            "contingency_cost":
                pricing.contingency_cost,

            "total_cost":
                pricing.total_cost,

            "recommended_price":
                pricing.recommended_price,

            "expected_profit":
                pricing.expected_profit,

            "expected_margin":
                pricing.expected_margin,

        },

        "historical_estimation_variance":
            request.historical_estimation_variance,

        "risks": [

            {
                "risk_type":
                    risk.risk_type,

                "severity":
                    risk.severity,

                "message":
                    risk.message,

                "recommendation":
                    risk.recommendation,
            }

            for risk in risks
        ],
    }


    
    ai_analysis = analyze_quote_with_ai(
        quote_data,
        historical_evidence=historical_evidence,
    )

    customer = None

    if request.customer_email:
        customer = (
            db.query(Customer)
            .filter(
                Customer.email == request.customer_email,
            )
            .first()
        )

    if customer is None:
        customer = Customer(
            name=request.customer_name,
            email=request.customer_email,
            company=request.customer_name,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

    quote_record = Quote(
        customer_id=customer.id,
        service_type=request.service_type,
        project_name=request.project_name,
        labor_hours=request.labor_hours,
        labor_rate=request.labor_rate,
        material_cost=request.material_cost,
        overhead_rate=request.overhead_rate,
        contingency_rate=request.contingency_rate,
        target_margin=request.target_margin,
        total_cost=pricing.total_cost,
        recommended_price=pricing.recommended_price,
        proposed_price=pricing.recommended_price,
        expected_profit=pricing.expected_profit,
        expected_margin=pricing.expected_margin,
        decision=ai_analysis.get("decision"),
    )

    db.add(quote_record)
    db.commit()
    db.refresh(quote_record)

    return {
        **quote_data["pricing"],
        "risks": quote_data["risks"],
        "ai_analysis": ai_analysis,
    }