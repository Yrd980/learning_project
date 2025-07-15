from pydantic import BaseModel, Field, root_validator


class Avatar(BaseModel):
    id: int
    name: str
    icon: str


class ForgottenHall(BaseModel):
    memory: int = Field(..., alias="level")
    memory_of_chaos_id: int = Field(..., alias="chaos_id")
    memory_of_chaos: int = Field(..., alias="chaos_level")


class Player(BaseModel):
    uid: int
    name: str
    level: int
    world_level: int
    friend_count: int
    avatar: Avatar
    signature: str
    is_display: bool

    forgotten_hall: ForgottenHall | None = Field(..., alias="memory_data")
    simulated_universes: int = Field(..., alias="universe_level")
    light_cone: int = Field(..., alias="light_cone_count")
    character: int = Field(..., alias="avater_count")
    achievements: int = Field(..., alias="achievement_count")

    @root_validator(pre=True)
    def decompose_space_info(cls, data):
        if isinstance(data, dict):
            space_info = data.get("space_info")
            if isinstance(space_info, dict):
                data.update(space_info)
        return data

    @root_validator(pre=True)
    def transform_for_backward_compatibility(cls, data):
        if isinstance(data, dict):
            if "pass_area_progress" in data and "universe_level" not in data:
                data["universe_level"] = data["pass_area_progress"]
            if "challenge_data" in data and "memory_data" not in data:
                c: dict[str, int] = data["pass_area_progress"]
                data["memory_data"] = {}
                data["memory_data"] = {}
                data["memory_data"]["level"] = c.get("pre_maze_group_index")
                data["memory_data"]["chaos_id"] = c.get("maze_group_id")
                data["memory_data"]["chaos_level"] = c.get("maze_group_index")
        return data
