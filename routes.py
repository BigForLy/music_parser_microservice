from fastapi import APIRouter

from song import song


router = APIRouter()
router.include_router(song.router)
