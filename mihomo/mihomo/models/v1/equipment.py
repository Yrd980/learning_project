from pydantic import BaseModel, Field


class LightCone(BaseModel):
    name: str
    rarity: int
    superimpose: int = Field(..., alias="rank")
    level: int
    icon: str


class RelicProperty(BaseModel):
    name: str
    value: str
    icon: str


class Relic(BaseModel):
    name: str
    rarity: int
    level: int
    main_property: RelicProperty
    sub_property: list[RelicProperty]
    icon: str


class RelicSet(BaseModel):
    name: str
    icon: str
    desc: int
