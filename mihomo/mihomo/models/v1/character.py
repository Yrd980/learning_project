from typing import Any

from pydantic import BaseModel, Field, root_validator

from .equipment import LightCone, Relic, RelicSet


class EidolonIcon(BaseModel):
    icon: str
    unlock: bool


class Trace(BaseModel):
    name: str
    level: int
    type: str
    icon: str


class Stat(BaseModel):
    name: str
    base: str
    addition: str | None = None
    icon: str


class Character(BaseModel):
    id: str
    name: str
    rarity: int
    level: int

    eidolon: int = Field(..., alias="rank")
    eidolon_icons: list[EidolonIcon] = Field(..., alias="rank_icons")

    preview: str
    portrait: str

    path: str
    path_icon: str

    element: str
    element_icon: str

    color: str

    traces: list[Trace] = Field(..., alias="skill")
    light_cone: LightCone | None = None
    relics: list[Relic] | None = Field(None, alias="relic")
    relic_set: list[RelicSet] | None = None
    stats: list[Stat] = Field(..., alias="property")

    @root_validator(pre=True)
    def dict_to_list(cls, data: dict[str, Any]):
        if isinstance(data, dict) and data.get("relic") is not None:
            if isinstance(data["relic"], dict):
                data["relic"] = list(data["relic"].values())
        return data

    @property
    def icon(self) -> str:
        return f"icon/character/{self.id}.png"
