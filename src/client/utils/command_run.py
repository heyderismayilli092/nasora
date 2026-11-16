import os
import asyncio
import httpx
from pathlib import Path


# function for sending files to the server
async def command_run(comm: str, server_url: str, directory: str = "."):
    remote_path = Path(directory)
    if not os.path.exists(remote_path):
        raise FileNotFoundError(directory)

    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    if not comm:
        raise Exception("Enter a command !")

    print("command: ", comm)
    print("remote path: ", directory)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/command",
            data={
                "directory": remote_path,
                "command": comm,
            }
        )

        response.raise_for_status()
        result = response.json()
        if response.status_code != 200:
            raise Exception(result.get("details", "Command run failed"))
    return result

