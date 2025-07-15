from pydantic import BaseModel


class Element(BaseModel):
    id: str
    name: str
    color: str
    icon: str


class Path(BaseModel):
    id: str
    name: str
    icon: str


class Trace(BaseModel):
    id: int
    name: str
    level: int
    max_level: int
    element: Element | None = None
    type: str
    type_text: str
    effect: str
    effect_text: str
    simple_desc: str
    desc: str
    icon: str


class TraceTreeNode(BaseModel):
    id: int
    level: int
    max_level: int
    icon: str
    anchor: str
    parent: int | None = None
