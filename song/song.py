from fastapi import APIRouter

from .parser import SoupHref, construct_building
from .models import Song


router = APIRouter()


@router.post("/v1/song/")
async def get_link(song: Song):
    # result = await construct_building(SoupHref, song.name)
    return {"url": await construct_building(SoupHref, song.name)}
