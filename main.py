import asyncio
from jutsu import JutSu, get_link_and_download


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

    for episode in episodes:
        print(f"{episode.season} - {episode.name}")

    coros = [
        asyncio.create_task(get_link_and_download(jutsu, episode, res))
        for episode in episodes
    ]

    if download_type == "1":
        for coro in coros:
            await coro

    elif download_type == "2":
        await asyncio.gather(*coros)

    await jutsu.close()


if __name__ == "__main__":
    asyncio.run(main())
