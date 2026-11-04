import os
import json
import uuid
import hashlib
import asyncio
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from utils import config

upload_router = APIRouter(prefix="/upload", tags=["Upload"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = Path(output["publish-path"]).resolve()

# upload metadata directory
UPLOAD_ROOT = publishfolder / ".nasora" / "uploads"
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

# upload locks (single-process protection)
upload_locks = {}


# --- helper functions ---
def get_upload_lock(upload_id: str):
    if upload_id not in upload_locks:
        upload_locks[upload_id] = asyncio.Lock()
    return upload_locks[upload_id]


def get_metadata_path(upload_id: str):
    try:
        upload_uuid = uuid.UUID(upload_id)
    except ValueError:
        raise HTTPException(400, "Invalid upload ID")

    return UPLOAD_ROOT / str(upload_uuid) / "metadata.json"


def read_metadata(upload_id: str):
    path = get_metadata_path(upload_id)
    if not path.is_file():
        raise HTTPException(404, "Upload session not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_metadata(upload_id: str, metadata: dict):
    path = get_metadata_path(upload_id)
    temp_path = path.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_path, path)


def get_destination(directory: str, filename: str):
    # filename validation
    if not filename or filename in (".", ".."):
        raise HTTPException(400, "Invalid filename")

    if Path(filename).name != filename or "/" in filename or "\\" in filename:
        raise HTTPException(400, "Invalid filename")

    # directory validation
    if not directory or directory in ("", "."):
        target_dir = publishfolder
    else:
        relative_dir = Path(directory)
        if relative_dir.is_absolute() or ".." in relative_dir.parts:
            raise HTTPException(400, "Invalid directory")

        target_dir = (publishfolder / relative_dir).resolve()

    # prevent path traversal and symlink escape
    if not target_dir.is_relative_to(publishfolder):
        raise HTTPException(403, "Directory outside publish folder")

    if not target_dir.is_dir():
        raise HTTPException(404, "Destination directory not found")

    final_path = target_dir / filename
    return target_dir, final_path


def get_part_path(metadata: dict):
    _, final_path = get_destination(
        metadata["directory"],
        metadata["filename"]
    )
    return final_path.with_name(f".{metadata['filename']}.{metadata['upload_id']}.part")


def calculate_sha256(filepath: Path):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(4 * 1024 * 1024)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def calculate_total_chunks(filesize: int, chunk_size: int):
    return (filesize + chunk_size - 1) // chunk_size
# -------------------------------


# initialize upload
@upload_router.post("/init")
async def upload_init(
    filename: str = Form(...),
    directory: str = Form("."),
    filesize: int = Form(...),
    chunk_size: int = Form(20 * 1024 * 1024),
    sha256: str = Form(...)
):

    # checking
    if filesize <= 0:
        raise HTTPException(400, "Invalid file size")

    if chunk_size <= 0 or chunk_size > 100 * 1024 * 1024:
        raise HTTPException(400, "Invalid chunk size")

    if len(sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in sha256):
        raise HTTPException(400, "Invalid SHA256")

    _, final_path = get_destination(directory, filename)

    if final_path.exists():
        raise HTTPException(409, "File already exists")

    # search for an existing matching upload
    for metadata_file in UPLOAD_ROOT.glob("*/metadata.json"):
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                old = json.load(f)

            if (old["filename"] == filename
                and old["directory"] == directory
                and old["filesize"] == filesize
                and old["sha256"] == sha256
                and old["chunk_size"] == chunk_size
                and old["status"] == "uploading"
            ):
                part_path = get_part_path(old)
                if part_path.is_file():
                    return {"status": True, "upload_id": old["upload_id"], "total_chunks": old["total_chunks"], "details": "Existing upload session found"}

        except (KeyError, ValueError, OSError):
            continue

    # create new upload session
    upload_id = str(uuid.uuid4())
    session_dir = UPLOAD_ROOT / upload_id
    session_dir.mkdir(parents=True, exist_ok=False)

    metadata = {
        "upload_id": upload_id,
        "filename": filename,
        "directory": directory,
        "filesize": filesize,
        "chunk_size": chunk_size,
        "total_chunks": calculate_total_chunks(filesize, chunk_size),
        "sha256": sha256.lower(),
        "received_chunks": [],
        "status": "uploading"
    }

    write_metadata(upload_id, metadata)
    part_path = get_part_path(metadata)

    # preallocate the temporary file
    with open(part_path, "wb") as f:
        f.truncate(filesize)
        f.flush()
        os.fsync(f.fileno())

    return {"status": True, "upload_id": upload_id, "total_chunks": metadata["total_chunks"], "details": "Upload initialized"}


# upload status
@upload_router.post("/status")
async def upload_status(
    upload_id: str = Form(...)
):
    metadata = read_metadata(upload_id)
    received = set(metadata["received_chunks"])
    missing = [i for i in range(metadata["total_chunks"]) if i not in received]
    return {"status": True, "upload_id": upload_id, "upload_status": metadata["status"], "total_chunks": metadata["total_chunks"], "received_chunks": sorted(received), "missing_chunks": missing}


# receive chunk
@upload_router.post("/chunk")
async def upload_chunk(
    upload_id: str = Form(...),
    chunk_index: int = Form(...),
    chunk_sha256: str = Form(...),
    chunk_data: UploadFile = File(...)
):
    lock = get_upload_lock(upload_id)
    async with lock:
        metadata = read_metadata(upload_id)
        if metadata["status"] != "uploading":
            raise HTTPException(409, "Upload is not active")

        total_chunks = metadata["total_chunks"]
        if not 0 <= chunk_index < total_chunks:
            raise HTTPException(400, "Invalid chunk index")

        if len(chunk_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in chunk_sha256):
            raise HTTPException(400, "Invalid chunk SHA256")

        chunk = await chunk_data.read()
        expected_size = min(metadata["chunk_size"], metadata["filesize"] - (chunk_index * metadata["chunk_size"]))

        if len(chunk) != expected_size:
            raise HTTPException(400, "Invalid chunk size")

        actual_hash = hashlib.sha256(chunk).hexdigest()

        if actual_hash.lower() != chunk_sha256.lower():
            raise HTTPException(422, "Chunk SHA256 mismatch")

        # write chunk at its byte offset
        part_path = get_part_path(metadata)
        offset = chunk_index * metadata["chunk_size"]

        with open(part_path, "r+b") as f:
            f.seek(offset)
            f.write(chunk)
            f.flush()
            os.fsync(f.fileno())

        # update received chunks
        received = set(metadata["received_chunks"])
        received.add(chunk_index)
        metadata["received_chunks"] = sorted(received)

        write_metadata(upload_id, metadata)
        return {"status": True, "chunk_index": chunk_index, "received": len(received), "total_chunks": total_chunks}


# finalize upload
@upload_router.post("/finalize")
async def upload_finalize(
    upload_id: str = Form(...)
):
    lock = get_upload_lock(upload_id)
    async with lock:
        metadata = read_metadata(upload_id)
        if metadata["status"] == "completed":
            return {"status": True, "details": "Upload already completed"}

        received = set(metadata["received_chunks"])
        expected = set(range(metadata["total_chunks"]))

        if received != expected:
            missing = sorted(expected - received)
            return {"status": False, "details": "Upload is incomplete", "missing_chunks": missing}

        part_path = get_part_path(metadata)

        _, final_path = get_destination(metadata["directory"], metadata["filename"])

        if not part_path.is_file():
            raise HTTPException(404, "Temporary file not found")

        if part_path.stat().st_size != metadata["filesize"]:
            raise HTTPException(422, "File size mismatch")

        # verify complete file
        actual_hash = calculate_sha256(part_path)

        if actual_hash != metadata["sha256"]:
            # allow client to resend all chunks
            metadata["received_chunks"] = []
            write_metadata(upload_id, metadata)

            raise HTTPException(422, "Final SHA256 mismatch")

        if final_path.exists():
            raise HTTPException(409, "Destination file already exists")

        # atomic rename
        os.replace(part_path, final_path)

        # mark session completed
        metadata["status"] = "completed"
        write_metadata(upload_id, metadata)

        # remove upload metadata
        session_dir = get_metadata_path(upload_id).parent
        shutil.rmtree(session_dir, ignore_errors=True)
        upload_locks.pop(upload_id, None)

        return {"status": True, "details": "Upload completed successfully", "filename": metadata["filename"], "filesize": metadata["filesize"], "sha256": actual_hash}

