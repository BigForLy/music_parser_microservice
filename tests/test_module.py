import asyncio
from dataclasses import dataclass
from api.app.parser import criterion_truth, get_href_to_url, get_link_to_download_song
import pytest

from api.const import SEARCH_LINK


@pytest.fixture()
def download_text() -> str:
    return "DOWNLOAD MP3:"


@pytest.fixture(scope="class")
def fixture_class_for_example1(request):
    @dataclass
    class Music:
        text: str
        text_enother: str  # значение которое может появляться в поиске
        music_page_url: str
        url_download: str

    request.cls.music = Music(
        text='Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")',
        text_enother="Madison Beer - I Have Never Felt More Alive",
        music_page_url="https://connectloaded.com/madison-beer-i-have-never-felt-more-alive-from-the-feature-film-fall/",
        url_download="https://connectloaded.xyz/uploads/2022/07/Madison_Beer_-_I_Have_Never_Felt_More_Alive_from_the_feature_film_Fall_-CONNECTLOADED.COM.mp3",
    )


@pytest.mark.usefixtures("fixture_class_for_example1")
class TestDownloadSongExample1:
    def test_get_download_song(self):
        async def _inner() -> str:
            return await get_link_to_download_song(self.music.text)

        result: str = asyncio.run(_inner())
        assert result == self.music.url_download, result

    def test_get_href_to_music_page(self):
        url: str = SEARCH_LINK + self.music.text

        async def _inner() -> str:
            return await get_href_to_url(url, self.music.text, rel="bookmark")

        result: str = asyncio.run(_inner())
        assert result == self.music.music_page_url, result

    def test_get_href_to_download_music(self, download_text):
        async def _inner() -> str:
            return await get_href_to_url(self.music.music_page_url, download_text)

        result: str = asyncio.run(_inner())
        assert result == self.music.url_download, result

    def test_criterion_truth_future_success(self):
        assert criterion_truth(self.music.text, self.music.text) == True

    def test_criterion_truth_future_failure(self):
        assert criterion_truth(self.music.text, self.music.text_enother) == True