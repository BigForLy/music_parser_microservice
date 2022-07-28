from api.app.parser import get_href_to_url, get_link_to_download_song
import asyncio

from api.const import SEARCH_LINK


def test_download_madison_beer_song():
    song_name = (
        'Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")'
    )

    url = "https://connectloaded.xyz/uploads/2022/07/Madison_Beer_-_I_Have_Never_Felt_More_Alive_from_the_feature_film_Fall_-CONNECTLOADED.COM.mp3"

    async def _inner() -> str:
        return await get_link_to_download_song(song_name)

    result: str = asyncio.run(_inner())
    assert result == url, result


def test_get_href_to_url_music_page():
    find_text = 'Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")'
    url: str = (
        SEARCH_LINK
        + find_text
    )

    async def _inner() -> str:
        return await get_href_to_url(url, find_text, rel="bookmark")

    result: str = asyncio.run(_inner())
    assert (
        result
        == "https://connectloaded.com/madison-beer-i-have-never-felt-more-alive-from-the-feature-film-fall/"
    ), result


# def test_download_pressurelicious_song():
#     song_name = "Megan Thee Stallion, Future - Pressurelicious (feat. Future)"
#     url = "https://connectloaded.xyz/uploads/2022/07/Megan_Thee_Stallion_feat_Future_-_Pressurelicious-CONNECTLOADED.COM.mp3"

#     async def _inner() -> str:
#         return await get_link_to_download_song(song_name)

#     result: str = asyncio.run(_inner())
#     assert result == url, result
