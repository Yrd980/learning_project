from typing import Final, TypeVar

from .models import StarrailInfoParsed
from .models.v1 import StarrailInfoParsedV1

RawData = TypeVar("RawData")
ParsedData = TypeVar("ParsedData", StarrailInfoParsed, StarrailInfoParsedV1)

ASSET_URL: Final[str] = "https://raw.githubusercontent.com/Mar-7th/StarRail/master"


def remove_empty_dict(data: RawData) -> RawData:
    if isinstance(data, dict):
        for key in data.keys():
            data[key] = None if (data[key] == {}) else remove_empty_dict(data[key])
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = remove_empty_dict(data[i])
    return data


def replace_icon_name_with_url(data: RawData) -> RawData:
    if isinstance(data, dict):
        for key in data.keys():
            data[key] = replace_icon_name_with_url(data[key])
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = replace_icon_name_with_url(data[i])
    elif isinstance(data, str):
        if ".png" in data:
            data = ASSET_URL + "/" + data
    return data


def replace_trailblazer_name(data: StarrailInfoParsedV1) -> StarrailInfoParsedV1:
    for i in range(len(data.characters)):
        if data.characters[i].name == r"{NICKNAME}":
            data.characters[i].name = data.player.name
    return data


def remove_duplicate_character(data: ParsedData) -> ParsedData:
    new_characters = []
    characters_ids: set[str] = set()
    for character in data.characters:
        if character.id not in characters_ids:
            new_characters.append(character)
            characters_ids.add(character.id)
    data.characters = new_characters
    return data


def merge_character_data(new_data: ParsedData, old_data: ParsedData) -> ParsedData:
    for character in old_data.characters:
        new_data.characters.append(character)
    new_data = remove_duplicate_character(new_data)
    return new_data
