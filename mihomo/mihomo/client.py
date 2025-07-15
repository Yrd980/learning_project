import typing
from enum import Enum

import aiohttp

from . import tools
from .errors import HttpRequestError, InvalidParams, UserNotFound
from .models import StarrailInfoParsed
from .models.v1 import StarrailInfoParsedV1


class Language(Enum):
    CHT = "cht"
    CHS = "cn"
    DE = "de"
    EN = "en"
    ES = "es"
    FR = "fr"
    ID = "id"
    JP = "jp"
    KR = "kr"
    PT = "pt"
    RU = "ru"
    TH = "th"
    VI = "vi"


class MihomoAPI:
    BASE_URL: typing.Final[str] = "https://api.mihomo.me/sr_info_parsed"
    ASSET_URL: typing.Final[str] = (
        "https://raw.githubusercontent.com/Mar-7th/StarRailRes/master"
    )

    def __init__(self, language: Language = Language.CHT):
        self.lang = language

    async def request(
        self,
        uid: int | str,
        language: Language,
        *,
        params: dict[str, str] = {},
    ) -> typing.Any:
        url = self.BASE_URL + "/" + str(uid)
        params.update({"lang": language.value})

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                match response.status:
                    case 200:
                        return await response.json(encoding="utf-8")
                    case 400:
                        try:
                            data = await response.json(encoding="utf-8")
                        except:
                            raise InvalidParams()
                        else:
                            if isinstance(data, dict) and (
                                detail := data.get("detail")
                            ):
                                raise InvalidParams(detail)
                            raise InvalidParams()
                    case 404:
                        raise UserNotFound()
                    case _:
                        raise HttpRequestError(response.status, str(response.reason))

    async def fetch_user(
        self,
        uid: int,
        *,
        replace_icon_name_with_url: bool = False,
    ) -> StarrailInfoParsed:
        data = await self.request(uid, self.lang)
        if replace_icon_name_with_url is True:
            data = tools.replace_icon_name_with_url(data)
        data = StarrailInfoParsed.parse_obj(data)
        return data

    async def fetch_user_v1(
        self,
        uid: int,
        *,
        replace_icon_name_with_url: bool = False,
    ) -> StarrailInfoParsedV1:
        data = await self.request(uid, self.lang, params={"version": "v1"})
        data = tools.remove_empty_dict(data)
        if replace_icon_name_with_url is True:
            data = tools.replace_icon_name_with_url(data)
        data = StarrailInfoParsedV1.parse_obj(data)
        data = tools.replace_trailblazer_name(data)
        return data

    def get_icon_url(self, icon: str) -> str:
        return self.ASSET_URL + "/" + icon
