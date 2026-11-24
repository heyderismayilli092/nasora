import os
import asyncio
import httpx
from pathlib import Path


# enables the downloading of files from a shared folder
async def download(path: str, filename: str, server_url: str, save_dir: str):
    base_url = server_url.rstrip("/")
    fullpath = os.path.join(path, filename)
    local_save_path = os.path.join(save_dir, filename)
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        # streams are used to avoid loading large files into RAM
        async with client.stream(
            "POST",
            f"{base_url}/download",
            data={"fullpath": fullpath}
        ) as response:

            if response.status_code != 200:
                await response.aread()
                try:
                    error_detail = response.json().get("detail", response.text)
                except Exception:
                    error_detail = response.text
                raise Exception(f"Download error ({response.status_code}): {error_detail}")

            # the incoming pieces are being written to the disk
            os.makedirs(save_dir, exist_ok=True)
            with open(local_save_path, "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)
            print(f"File saved: {local_save_path}")

    return os.path.basename(local_save_path)


# function for sending files to the server
async def info_file(path: str, filename: str, server_url: str):
    fullpath = os.path.join(path, filename)
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/info_file",
            data={"fullpath": fullpath}
        )

        result = response.json()
        if response.status_code != 200:
            raise Exception(result.get("details", "File information could not be retrieved !"))

    return result


# delete file in publish folder
async def delete_file(path: str, filename: str, server_url: str):
    fullpath = os.path.join(path, filename)
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/delete_file",
            data={"fullpath": fullpath}
        )
        result = response.json()

        if response.status_code != 200:
            error_detail = result.get("detail")
            raise Exception(error_detail)
        else:
            return result

