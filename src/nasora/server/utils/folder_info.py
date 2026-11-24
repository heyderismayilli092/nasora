import os
import stat
import pwd
import grp
import shutil
import json
from datetime import datetime


def get_folder_info(path):
    path = os.path.abspath(path)
    info = os.stat(path)  # folder informations
    total_size = 0
    file_count = 0
    folder_count = 0

    # attempting to calculate the total size, including subfolders
    for root, dirs, files in os.walk(path):
        folder_count += len(dirs)
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
                file_count += 1
            except OSError:
                pass

    try:
        owner = pwd.getpwuid(info.st_uid).pw_name  # retrieve folder owner
    except KeyError:
        owner = str(info.st_uid)

    try:
        group = grp.getgrgid(info.st_gid).gr_name  # retrieve folder group
    except KeyError:
        group = str(info.st_gid)

    disk = shutil.disk_usage(path)

    return {
        "path": path,
        "name": os.path.basename(path),
        "permissions": {
            "symbolic": stat.filemode(info.st_mode),
            "octal": oct(stat.S_IMODE(info.st_mode))
        },
        "ownership": {
            "owner": owner,
            "group": group,
            "uid": info.st_uid,
            "gid": info.st_gid
        },
        "size": { total_size },
        "contents": {
            "files": file_count,
            "directories": folder_count
        },
        "timestamps": {
            "created": datetime.fromtimestamp(info.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(info.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(info.st_atime).isoformat()
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free
        }
    }

