import os
import asyncio
import httpx
from pathlib import Path


# retrieve server info
async def serverinfo(server_url: str):
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{base_url}/serverinfo")

        result = response.json()
        if response.status_code != 200:
            raise Exception(result.get("details", "server information not be retrieved"))
    return result

