import asyncio
from jutsu import JutSu, get_link_and_download

from more_itertools import batched


async def main():
    slug = input("Enter the link or name: ")

    if slug.startswith("http"):
        slug = slug.split("/")[3]

    res = input("Enter the resolution (1080, 720, 480, 360): ")

    download_type = input("Download synchronously or asynchronously? (1, 2): ")

    if res not in ("1080", "720", "480", "360"):
        return print("Enter the correct resolution!")

    jutsu = JutSu(slug)

    episodes = await jutsu.get_all_episodes()

    crt_eps = sum(ep for ep in episodes if ep.season == "season-1")

    coros = [
        asyncio.create_task(get_link_and_download(jutsu, episode, res))
        for episode in episodes
    ]

    coros = batched(coros, crt_eps)

    if download_type == "1":
        for coro in coros:
            for cor in coro:
                await cor

    elif download_type == "2":
        for coro in coros:
            await asyncio.gather(*coros)

    await jutsu.close()


if __name__ == "__main__":
    asyncio.run(main())
