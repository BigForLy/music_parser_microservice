from typing import List
from api.const import SEARCH_LINK
from api.services import get_requests
import httpx
from bs4 import BeautifulSoup, element, SoupStrainer


async def download_song():
    pass


async def get_link_to_download_song(song_name: str) -> str:
    url: str = SEARCH_LINK + song_name

    music_page_url = await get_href_to_url(url, song_name, rel="bookmark")

    href = await get_href_to_url(music_page_url, song_name)
    print(href)


async def get_href_to_url(url: str, find_text: str, **kwargs) -> str:
    search_response: httpx.Response = await get_requests(url)  # TODO: raise exception
    def _inner(item: element.Tag):
        isalnum_find_text: str = "".join(char for char in find_text if char.isalnum())

    return await SoupHref(search_response.text, find_text, **kwargs).get_href


class SoupHref:
    def __init__(self, html_text: str, song_name: str, lambda_=None, **kwargs) -> None:
        isalnum_song_name: str = "".join(char for char in song_name if char.isalnum())

        def _inner(item: element.Tag) -> bool:
            return (
                all(
                    [
                        True
                        if item.has_attr(key) and item.get(key)[0] == value
                        else False
                        for key, value in kwargs.items()
                    ]
                )
                and "".join(char for char in item.get_text() if char.isalnum())
                == isalnum_song_name
                and (lambda_ is None or lambda_ is not None and lambda_(True))
            )

        soup = BeautifulSoup(html_text, "html.parser", parse_only=SoupStrainer("a"))
        # получаем список ссылок на страницу загрузки
        search_href: List[str] = [item.get("href") for item in soup if _inner(item)]
        assert len(search_href) == 1, search_href
        self.__href: str = search_href[0]

    @property
    async def get_href(self) -> str:
        return self.__href
