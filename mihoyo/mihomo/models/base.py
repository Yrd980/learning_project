from pydantic import BaseModel, Field

from .character import Character
from .player import Player


class StarrailInfoParsed(BaseModel):
    player: Player
    character: list[Character]
