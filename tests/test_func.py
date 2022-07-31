from fastapi.testclient import TestClient

from main import app

client: TestClient = TestClient(app)


def test_main_page():
    response = client.get("/")
    assert response.status_code == 404


def test_href_song():
    response = client.post(
        "/api/v1/song/",
        json={
            "name": 'Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")'
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "url": "https://connectloaded.xyz/uploads/2022/07/Madison_Beer_-_I_Have_Never_Felt_More_Alive_from_the_feature_film_Fall_-CONNECTLOADED.COM.mp3"
    }, response.text
