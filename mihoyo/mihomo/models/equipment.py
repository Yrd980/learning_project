from pydantic import BaseModel, Field

from .combat import Path
from .stat import Attribute, MainAffix, Property, SubAffix


class LightCone(BaseModel):
    id: int
    name: str
    rarity: int
    superimpose: int = Field(..., alias="rank")
    level: int
    ascension: int = Field(..., alias="promotion")
    icon: str
    preview: str
    portrait: str
    path: Path
    attributes: list[Attribute]
    properties: list[Property]

    @property
    def max_level(self) -> int:
        return 20 + 10 * self.ascension


class Relic(BaseModel):
    id: int
    name: str
    set_id: int
    set_name: str
    rarity: int
    level: int
    main_affix: MainAffix
    sub_affixes: list[SubAffix] = Field([], alias="sub_affix")
    icon: str


class RelicSet(BaseModel):
    id: int
    name: str
    icon: str
    num: int
    desc: str
    properties: list[Property]
