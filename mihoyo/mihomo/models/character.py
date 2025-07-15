from pydantic import BaseModel, Field

from .combat import Element, Path, Trace, TraceTreeNode
from .equipment import LightCone, Relic, RelicSet
from .stat import Attribute, Property


class Character(BaseModel):
    id: str
    name: str
    rarity: str
    level: int
    ascension: int = Field(..., alias="promotion")
    eidolon: int = Field(..., alias="rank")
    eidolon_icons: list[str] = Field([], alias="rank_icons")

    icon: str
    preview: str
    portrait: str

    path: Path
    element: Element
    traces: list[Trace] = Field([], alias="skills")
    trace_tree: list[TraceTreeNode] = Field([], alias="skill_trees")

    light_cone: LightCone | None = None
    relics: list[Relic] = []
    relic_sets: list[RelicSet] = []

    attributes: list[Attribute]
    additions: list[Attribute]
    properties: list[Property]

    @property
    def max_level(self) -> int:
        return 20 + 10 * self.ascension
