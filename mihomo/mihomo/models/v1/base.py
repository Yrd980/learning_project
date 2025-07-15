from pydantic import BaseModel, Field

from .character import Character
from .player import Player, PlayerSpaceInfo


class StarrailInfoParsedV1(BaseModel):

    player: Player
    player_details: PlayerSpaceInfo = Field(..., alias="PlayerSpaceInfo")
    characters: list[Character]
