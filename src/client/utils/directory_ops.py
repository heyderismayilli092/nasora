import os
import asyncio
import httpx
from pathlib import Path


# lists the publish folder
async def directory_list(server_url: str):
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{base_url}/directory_list/")
        response.raise_for_status()
        result = response.json()

        if response.status_code != 200:
            error_detail = result.get("detail")
            raise Exception(error_detail)
        else:
            return result


# create folder in publish folder
async def create_folder(foldername: str, server_url: str):
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/create_folder",
            data={"foldername": foldername}
        )
        response.raise_for_status()
        result = response.json()

        if response.status_code != 200:
            error_detail = result.get("detail")
            raise Exception(error_detail)
        else:
            return result


# delete folder in publish folder
async def delete_folder(foldername: str, server_url: str):
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/delete_folder",
            data={"foldername": foldername}
        )
        response.raise_for_status()
        result = response.json()

        if response.status_code != 200:
            error_detail = result.get("detail")
            raise Exception(error_detail)
        else:
            return result


# displays information about the general folder or subfolders
async def info_folder(path: str, server_url: str):
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{base_url}/info_folder",
            data={"path": path}
        )

        result = response.json()
        if response.status_code != 200:
            raise Exception(result.get("details", "Folder information could not be retrieved !"))

    return result

