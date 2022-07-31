import warnings
import time
import asyncio

from song.services import SoupHref, construct_building


async def performance_test(name: str, n_count: int = 10):
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    async def download_song():
        await construct_building(SoupHref, name)

    tasks = [download_song() for _ in range(n_count)]

    start = time.time()

    await asyncio.gather(*tasks)

    end = time.time() - start
    print(f"\n{name = }")
    print(f"time {end:0.2f} seconds")
    print(f"mean time for 1 request: {end/10:0.2f} seconds")


class TestStress:
    def test_stress_testing(self):
        asyncio.run(
            performance_test(
                name=f'Madison Beer - I Have Never Felt More Alive (from the feature film "Fall")'
            )
        )
        # mean time for 1 request: 0.20 seconds
        assert True
