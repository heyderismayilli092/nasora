import os
import hashlib
import asyncio
import httpx
from pathlib import Path

# calculate complete file SHA256
async def file_sha256(filepath: str):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4 * 1024 * 1024)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


# calculate individual chunk SHA256
def chunk_sha256(data: bytes):
    return hashlib.sha256(data).hexdigest()


# function for sending files to the server
async def send_file(file_path: str, server_url: str, directory: str = "."):
    chunk_size = 20 * 1024 * 1024  # chunk size
    retries = 3  # retires

    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    filename = file_path.name
    filesize = file_path.stat().st_size
    base_url = server_url.rstrip("/")
    timeout = httpx.Timeout(300.0, connect=30.0)

    print(f"Preparing upload: {filename}")
    # calculate complete file hash
    sha256 = await asyncio.to_thread(lambda: hashlib.sha256(file_path.read_bytes()).hexdigest())
    async with httpx.AsyncClient(timeout=timeout) as client:

        # initialize upload
        response = await client.post(
            f"{base_url}/upload/init",
            data={
                "filename": filename,
                "directory": directory,
                "filesize": str(filesize),
                "chunk_size": str(chunk_size),
                "sha256": sha256,
            }
        )

        result = response.json()
        if response.status_code != 200:
            raise Exception(result.get("details", "Upload init failed"))

        upload_id = result["upload_id"]
        total_chunks = result["total_chunks"]

        print(f"upload ID: {upload_id}")
        print(f"total chunks: {total_chunks}")

        # get upload status
        response = await client.post(f"{base_url}/upload/status", data={"upload_id": upload_id})
        result = response.json()
        missing_chunks = result["missing_chunks"]
        print(f"remaining chunks: {len(missing_chunks)}")

        # send missing chunks
        with open(file_path, "rb") as file:
            for chunk_index in missing_chunks:
                offset = chunk_index * chunk_size
                file.seek(offset)
                chunk = file.read(chunk_size)
                current_hash = chunk_sha256(chunk)
                uploaded = False

                for attempt in range(1, retries + 1):
                    try:
                        response = await client.post(f"{base_url}/upload/chunk",
                            data={
                                "upload_id": upload_id,
                                "chunk_index": str(chunk_index),
                                "chunk_sha256": current_hash,
                            },
                            files={"chunk_data": (filename, chunk, "application/octet-stream")}
                        )
                        result = response.json()
                        if response.status_code != 200:
                            raise Exception("Chunk upload failed")
                        uploaded = True
                        break

                    except (httpx.HTTPError, Exception) as error:
                        print(f"Chunk {chunk_index} failed " f"(attempt {attempt}/{retries}): {error}")
                        if attempt < retries:
                            await asyncio.sleep(min(2 ** attempt, 10))

                if not uploaded:
                    raise Exception(f"could not upload chunk {chunk_index}")

                transferred = min((chunk_index + 1) * chunk_size, filesize)
                percentage = (transferred / filesize * 100 if filesize else 100)
                print(f"chunk {chunk_index + 1}/{total_chunks} | {percentage:.2f}%")

        # finalize upload
        response = await client.post(f"{base_url}/upload/finalize", data={"upload_id": upload_id})
        response.raise_for_status()
        result = response.json()

        if response.status_code != 200:
            raise Exception(result.get("details", "Upload finalization failed"))
        print("Upload completed successfully!")
        return result

