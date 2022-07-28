import httpx


async def get_requests(url: str) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        result: httpx.Response = await client.get(url)
        result.raise_for_status()
        return result
