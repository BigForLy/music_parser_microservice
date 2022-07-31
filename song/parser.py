from __future__ import annotations
from typing import List
from .const import SEARCH_LINK
from .services import criterion_truth, get_requests
import httpx
import functools
from bs4 import BeautifulSoup, element, SoupStrainer


async def construct_building(cls: SoupHref, song_name: str):
    url: str = SEARCH_LINK + song_name

    soup: SoupHref = cls(url)
    await soup.get_href_to_url(song_name, rel="bookmark")
    await soup.get_href_to_url("DOWNLOAD MP3:")
    return soup.url


class SoupHref:
    def __init__(self, url: str) -> None:
        self.__url: str = url

    async def get_href_to_url(self, find_text: str, **kwargs) -> None:
        response: httpx.Response = await get_requests(self.url)  # TODO: raise exception

        inner = functools.partial(criterion_truth, find_text)
        self.__get_href(response.text, inner, **kwargs)

    def __get_href(self, html_text: str, lambda_=None, **kwargs) -> None:
        def _inner(item: element.Tag) -> bool:
            return all(
                [
                    True if item.has_attr(key) and item.get(key)[0] == value else False
                    for key, value in kwargs.items()
                ]
            ) and (lambda_ is None or lambda_ is not None and lambda_(item.get_text()))

        soup = BeautifulSoup(html_text, "html.parser", parse_only=SoupStrainer("a"))
        # получаем список ссылок на страницу загрузки
        search_href: List[str] = [item.get("href") for item in soup if _inner(item)]
        assert len(search_href) == 1, search_href
        self.__url: str = search_href[0]

    @property
    def url(self) -> str:
        return self.__url
