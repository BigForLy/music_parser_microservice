from typing import List, Generator
from api.const import SEARCH_LINK
from api.services import get_requests
import httpx
from bs4 import BeautifulSoup, element, SoupStrainer


async def get_link_to_download_song(song_name: str) -> str:
    url: str = SEARCH_LINK + song_name

    music_page_url = await get_href_to_url(url, song_name, rel="bookmark")

    href = await get_href_to_url(music_page_url, "DOWNLOAD MP3:")
    return href


async def get_href_to_url(url: str, find_text: str, **kwargs) -> str:
    response: httpx.Response = await get_requests(url)  # TODO: raise exception

    def _inner(item: element.Tag):
        isalnum_find_text: str = "".join(char for char in find_text if char.isalnum())
        if isalnum_find_text in "".join(
            char for char in item.get_text() if char.isalnum()
        ):
            return True
        else:
            return False

    # _inner = functools.partial(criterion_truth, find_text)

    return await SoupHref(response.text, _inner, **kwargs).get_href


def criterion_truth(desired: str, valid: str) -> bool:
    def _inner(find_text: str) -> Generator[str, None, None]:
        for word in find_text.split():
            yield "".join(char for char in word if char.isalnum())

    valid_words: List[str] = list(_inner(valid))
    result: List[bool] = [
        True if desired_word in valid_words else False
        for desired_word in _inner(desired)
    ]

    return True if sum(result) / len(result) > 0.5 else False


class SoupHref:
    def __init__(self, html_text: str, lambda_=None, **kwargs) -> None:
        def _inner(item: element.Tag) -> bool:
            return all(
                [
                    True if item.has_attr(key) and item.get(key)[0] == value else False
                    for key, value in kwargs.items()
                ]
            ) and (lambda_ is None or lambda_ is not None and lambda_(item))

        soup = BeautifulSoup(html_text, "html.parser", parse_only=SoupStrainer("a"))
        # получаем список ссылок на страницу загрузки
        search_href: List[str] = [item.get("href") for item in soup if _inner(item)]
        assert len(search_href) == 1, search_href
        self.__href: str = search_href[0]

    @property
    async def get_href(self) -> str:
        return self.__href
