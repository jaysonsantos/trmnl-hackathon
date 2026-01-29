from fastapi import FastAPI
import json
import aiohttp
import asyncio

app = FastAPI()

BASE_URL = "https://v6.bvg.transport.rest"


# session = aiohttp.ClientSession()


async def decode_address(session, address):
    async with session.get(
        f"{BASE_URL}/locations", params={"query": address, "results": 50}
    ) as response:
        rv = await response.json()
        print(rv)
        for possible in rv:
            if possible["type"] == "stop":
                return possible
        raise ValueError(f"No stop found for address {address} {rv}")


async def get_journey_info(session, from_, to_, arrival_time):
    params = {"from": from_, "to": to_, "results": 3, "stopovers": "true"}
    print(params)
    async with session.get(f"{BASE_URL}/journeys", params=params) as response:
        return await response.json()


@app.get("/")
def read_root():
    with open("mock.json", "r") as f:
        return json.load(f)


@app.get("/get-directions")
async def get_directions(from_address: str, to_address: str, arrival_time: str):
    async with aiohttp.ClientSession() as session:
        from_, to = await asyncio.gather(
            decode_address(session, from_address), decode_address(session, to_address)
        )
        return await get_journey_info(session, from_["id"], to["id"], arrival_time)


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
