import asyncio
from utils.send_file import send_file as _async_send_file
from utils.command_run import command_run as _async_commrun
from utils.directory_ops import directory_list as _async_dirlist
from utils.directory_ops import create_folder as _async_createfolder
from utils.directory_ops import delete_folder as _async_deletefolder
from utils.file_ops import download as _async_filedownload


# file selected by the user are being sent to the selected server
def send_file(filename: str, remotepath: str, ipaddr: str):
    try:
        return asyncio.run(
            _async_send_file(
                file_path=filename,
                server_url=f"http://{ipaddr}:2215/",
                directory=remotepath
            )
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e


# enables the execution of commands within a shared folder
def command(comm: str, remotepath: str, ipaddr: str):
    try:
        return asyncio.run(
            _async_commrun(
                comm=comm,
                server_url=f"http://{ipaddr}:2215/",
                directory=remotepath
            )
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e


# shared folder is being listed
def directory_list(ipaddr: str):
    try:
        return asyncio.run(
            _async_dirlist(server_url=f"http://{ipaddr}:2215/")
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e


# create new folder in shared folder
def create_folder(foldername: str, ipaddr: str):
    try:
        return asyncio.run(
           _async_createfolder(
                foldername=foldername,
                server_url=f"http://{ipaddr}:2215/"
            )
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e


# delete folder in shared folder
def delete_folder(foldername: str, ipaddr: str):
    try:
        return asyncio.run(
           _async_deletefolder(
                foldername=foldername,
                server_url=f"http://{ipaddr}:2215/"
            )
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e


# download file from shared folder
def download(path: str, filename: str, save_dir: str, ipaddr: str):
    try:
        return asyncio.run(
           _async_filedownload(
                path=path,
                filename=filename,
                save_dir=save_dir,
                server_url=f"http://{ipaddr}:2215/"
            )
        )
    except FileNotFoundError as e:
        return e
    except Exception as e:
        return e

