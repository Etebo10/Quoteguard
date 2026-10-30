from pydantic import BaseModel, EmailStr, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str | None
    phone: str | None
    company: str | None

    model_config = ConfigDict(from_attributes=True)