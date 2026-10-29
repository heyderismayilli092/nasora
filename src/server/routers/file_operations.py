# POST /download/
# File download endpoints scaffold

from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from utils import config, file_info
import os

# endpoints
downloadfile_router = APIRouter(prefix="/download", tags=["Download"])
infofile_router = APIRouter(prefix="/fileinfo", tags=["File Informations"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


@downloadfile_router.post("")
async def downloadfile(
    filename: str = Form(...)
):
    # check filename
    if not filename:
        return {"status": False, "details": "File name not provided !"}

    filepath = os.path.join(publishfolder, filename)  # file full path
    # check file avaliable
    if not os.path.exists(filepath):
        print("File to be downloaded could not be found !")
        return {"status": False, "details": "File to be downloaded could not be found !"}

    try:
        # download
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/octet-stream"  # general download type
        )
    except PermissionError:
        print("File cannot be downloaded due to permission restrictions !")
        return {"status": False, "details": "File cannot be downloaded due to permission restrictions !"}


# file informations
@infofile_router.post("")
async def fileinfo(
    filename: str = Form(...)
):
    # check filename
    if not filename:
        return {"status": False, "details": "File name not provided !"}

    filepath = os.path.join(publishfolder, filename)  # file full path
    # check file avaliable
    if not os.path.exists(filepath):
        print("File to be downloaded could not be found !")
        return {"status": False, "details": "File to be downloaded could not be found !"}

    output = file_info.get_file_info(filepath)
    return output



# main router
fileoperations_router = APIRouter()
fileoperations_router.include_router(downloadfile_router)
fileoperations_router.include_router(infofile_router)

