from fastapi import APIRouter

from .services import SoupHref, construct_building
from .models import Song


router = APIRouter()


@router.post("/v1/song/")
async def get_link(song: Song):
    soup = await construct_building(SoupHref, song.name)
    return {"url": soup.url}
