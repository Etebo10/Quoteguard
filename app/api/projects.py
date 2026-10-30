from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.customer import Customer
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse


router = APIRouter(prefix="/projects", tags=["Projects"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProjectResponse)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    if project_data.customer_id is not None:
        customer = db.query(Customer).filter(Customer.id == project_data.customer_id).first()
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")

    project = Project(
        customer_id=project_data.customer_id,
        name=project_data.name,
        service_type=project_data.service_type,
        estimated_labor_hours=project_data.estimated_labor_hours,
        actual_labor_hours=project_data.actual_labor_hours,
        estimated_material_cost=project_data.estimated_material_cost,
        actual_material_cost=project_data.actual_material_cost,
        quoted_price=project_data.quoted_price,
        final_price=project_data.final_price,
        status=project_data.status,
        completed_at=project_data.completed_at,
    )

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/customer/{customer_id}", response_model=list[ProjectResponse])
def get_customer_projects(customer_id: int, db: Session = Depends(get_db)):
    projects = db.query(Project).filter(Project.customer_id == customer_id).all()
    return projects
