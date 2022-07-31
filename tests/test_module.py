import asyncio
from dataclasses import dataclass
from song.services import (
    SoupHref,
    construct_building,
    criterion_truth,
)
import pytest

from song.const import SEARCH_LINK


@pytest.fixture()
def download_text() -> str:
    return "DOWNLOAD MP3:"


@dataclass
class Music:
    text: str
    text_enother: str  # значение которое может появляться в поиске
    music_page_url: str
    url_download: str


class AbstractTest:
    def test_get_href_to_music_page(self):
        url: str = SEARCH_LINK + self.music.text

        async def _inner() -> str:
            soup = SoupHref(url)
            await soup.get_href_to_url(self.music.text, rel="bookmark")
            return soup.url

        result: str = asyncio.run(_inner())
        assert result == self.music.music_page_url, result

    def test_get_href_to_download_music(self, download_text):
        async def _inner() -> str:
            soup = SoupHref(self.music.music_page_url)
            await soup.get_href_to_url(download_text)
            return soup.url

        result: str = asyncio.run(_inner())
        assert result == self.music.url_download, result

    def test_construct_building_download_music(self):
        async def _inner() -> str:
            return await construct_building(SoupHref, self.music.text)

        result: str = asyncio.run(_inner())
        assert result == self.music.url_download, result

    def test_criterion_truth_future_failure(self):
        assert criterion_truth(self.music.text, self.music.text_enother) == True


@pytest.fixture(scope="class")
def fixture_class_for_example1(request):

    request.cls.music = Music(
        text='Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")',
        text_enother="Madison Beer - I Have Never Felt More Alive",
        music_page_url="https://connectloaded.com/madison-beer-i-have-never-felt-more-alive-from-the-feature-film-fall/",
        url_download="https://connectloaded.xyz/uploads/2022/07/Madison_Beer_-_I_Have_Never_Felt_More_Alive_from_the_feature_film_Fall_-CONNECTLOADED.COM.mp3",
    )


@pytest.mark.usefixtures("fixture_class_for_example1")
class TestDownloadSongExample1(AbstractTest):
    pass


@pytest.fixture(scope="class")
def fixture_class_for_example2(request):
    request.cls.music = Music(
        text="Megan Thee Stallion, Future - Pressurelicious (feat. Future)",
        text_enother="Megan Thee Stallion – Pressurelicious Ft Future",
        music_page_url="https://connectloaded.com/megan-thee-stallion-pressurelicious-ft-future/",
        url_download="https://connectloaded.xyz/uploads/2022/07/Megan_Thee_Stallion_feat_Future_-_Pressurelicious-CONNECTLOADED.COM.mp3",
    )


@pytest.mark.usefixtures("fixture_class_for_example2")
class TestDownloadSongExample2(AbstractTest):
    pass
