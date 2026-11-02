# File Operations
# POST /download
# POST /file_info
# POST /file_delete


from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from utils import config, file_info
import os

# endpoints
downloadfile_router = APIRouter(prefix="/download", tags=["File Download"])
infofile_router = APIRouter(prefix="/file_info", tags=["File Informations"])
filedelete_router = APIRouter(prefix="/file_delete", tags=["File Delete"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


# file download
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
        print("File name not provided !")
        return {"status": False, "details": "File name not provided !"}

    filepath = os.path.join(publishfolder, filename)  # file full path
    # check file avaliable
    if not os.path.exists(filepath):
        print("File to be downloaded could not be found !")
        return {"status": False, "details": "File to be downloaded could not be found !"}

    output = file_info.get_file_info(filepath)
    return output


# file delete
@filedelete_router.post("")
async def filedelete(
    filename: str = Form(...)
):
    # check filename
    if not filename:
        print("File name not provided !")
        return {"status": False, "details": "File name not provided !"}

    filepath = os.path.join(publishfolder, filename)  # file full path
    # check file avaliable
    if not os.path.exists(filepath):
        print(f"'{filename}' not found !")
        return {"status": False, "details": f"'{filename}' not found !"}

    try:
        os.remove(filepath)  # removing file
        return {"status": True}
    except IsADirectoryError:
        print("The item you want to delete is not a file !")
        return {"status": False, "details": "The item you want to delete is not a file !"}
    except PermissionError:
        print("The file cannot be deleted due to permission restrictions !")
        return {"status": False, "details": "The file cannot be deleted due to permission restrictions !"}



# main router
fileoperations_router = APIRouter()
fileoperations_router.include_router(downloadfile_router)
fileoperations_router.include_router(infofile_router)
fileoperations_router.include_router(filedelete_router)

