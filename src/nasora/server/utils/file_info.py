import os
import stat
import hashlib
import magic
from pathlib import Path
from datetime import datetime


def get_file_info(file_path):
    path = Path(file_path).expanduser()
    file_stat = path.stat()  # retrieve file stats

    sha256 = hashlib.sha256()  # calculate sha256
    with path.open("rb") as file:  # it performs the operation without loading the entire file into memory
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256.update(chunk)

    # get file permissions in symbolic and numeric format
    permissions = stat.filemode(file_stat.st_mode)
    permission_octal = oct(stat.S_IMODE(file_stat.st_mode))

    # retrieve mime type
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_path)

    # informations
    return {
        "name": path.name,
        "absolute_path": str(path.resolve()),
        "parent_directory": str(path.parent.resolve()),
        "extension": path.suffix,
        "size_bytes": file_stat.st_size,
        "sha256": sha256.hexdigest(),
        "permissions": permissions,
        "permissions_octal": permission_octal,
        "owner_uid": file_stat.st_uid,
        "group_gid": file_stat.st_gid,
        "inode": file_stat.st_ino,
        "hard_links": file_stat.st_nlink,
        "device_id": file_stat.st_dev,
        "mime_type": mime_type,
        "created_or_changed_time": datetime.fromtimestamp(
            file_stat.st_ctime
        ).astimezone().isoformat(timespec="seconds"),
        "modified_time": datetime.fromtimestamp(
            file_stat.st_mtime
        ).astimezone().isoformat(timespec="seconds"),
        "accessed_time": datetime.fromtimestamp(
            file_stat.st_atime
        ).astimezone().isoformat(timespec="seconds"),
        "is_symlink": path.is_symlink(),
        "is_readable": os.access(path, os.R_OK),
        "is_writable": os.access(path, os.W_OK),
        "is_executable": os.access(path, os.X_OK),
    }

