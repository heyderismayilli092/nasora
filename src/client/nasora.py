import asyncio
from utils.send_file import send_file as _async_send_file
from utils.command_run import command_run as _async_commrun


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


#
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

