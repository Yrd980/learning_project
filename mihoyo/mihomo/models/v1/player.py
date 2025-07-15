from pydantic import BaseModel, Field


class Player(BaseModel):
    uid: str
    name: str
    level: str
    icon: str
    signiture: str


class ForgottenHall(BaseModel):
    memory: int | None = Field(..., alias="PreMazeGroupIndex")
    memory_of_chaos_id: int | None = Field(..., alias="MazeGroupID")
    memory_of_chaos: int | None = Field(None, alias="MazeGroupID")


class PlayerSpaceInfo(BaseModel):
    forgotten_hall: ForgottenHall | None = Field(..., alias="ChallengeData")
    simulated_universes: int = Field(0, alias="PassAreaProgress")
    light_cones: int = Field(0, alias="LightConeCount")
    characters: int = Field(0, alias="AvatarCount")
    achievements: int = Field(0, alias="AchievementCount")
