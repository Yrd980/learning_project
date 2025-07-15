from pydantic import BaseModel, Field


class Attribute(BaseModel):
    field: str
    name: str
    icon: str
    value: str
    displayed_value: str = Field(..., alias="displayed")
    is_percent: bool = Field(..., alias="percent")


class Property(BaseModel):
    type: str
    field: str
    name: str
    icon: str
    value: float
    displayed_value: str = Field(..., alias="displayed")
    is_percent: bool = Field(..., alias="percent")


class MainAffix(Property): ...


class SubAffix(MainAffix):
    count: int
    step: int
