# POST /download/
# File download endpoints scaffold

from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from utils import config
import os

router = APIRouter(prefix="/download", tags=["Download"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


@router.post("")
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

