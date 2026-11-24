# File Operations
# POST /download
# POST /info_file
# POST /delete_file
# POST /create_file


from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse
from nasora.server.utils import config, file_info
import os

# endpoints
downloadfile_router = APIRouter(prefix="/download", tags=["File Download"])
infofile_router = APIRouter(prefix="/info_file", tags=["File Informations"])
filedelete_router = APIRouter(prefix="/delete_file", tags=["File Delete"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


# file download
@downloadfile_router.post("")
async def downloadfile(
    fullpath: str = Form(...)
):
    # check file availability
    if not fullpath:
        raise HTTPException(status_code=404, detail="File path not provided !")

    filepath = os.path.join(publishfolder, fullpath)  # file full path
    filename = os.path.basename(fullpath)
    # check file avaliable
    if not os.path.exists(filepath):
        print("File to be downloaded could not be found !")
        raise HTTPException(status_code=404, detail="File to be downloaded could not be found !")

    try:
        # download
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/octet-stream"  # general download type
        )
    except PermissionError:
        print("File cannot be downloaded due to permission restrictions !")
        raise HTTPException(status_code=404, detail="File cannot be downloaded due to permission restrictions !")


# file informations
@infofile_router.post("")
async def fileinfo(
    fullpath: str = Form(...)
):
    # check file availability
    if not fullpath:
        print("File path not provided !")
        raise HTTPException(status_code=404, detail="File path not provided !")

    filepath = os.path.join(publishfolder, fullpath)  # file full path
    filename = os.path.basename(fullpath)

    # check file avaliable
    if not os.path.exists(filepath):
        print(f"'{filename}' not found !")
        raise HTTPException(status_code=404, detail=f"'{filename}' not found !")

    output = file_info.get_file_info(filepath)
    return output


# file delete
@filedelete_router.post("")
async def filedelete(
    fullpath: str = Form(...)
):
    # check check file availability
    if not fullpath:
        print("File path not provided !")
        raise HTTPException(status_code=404, detail="File path not provided !")

    filepath = os.path.join(publishfolder, fullpath)  # file full path
    filename = os.path.basename(fullpath)
    # check file avaliable
    if not os.path.exists(filepath):
        print(f"'{filename}' not found !")
        raise HTTPException(status_code=404, detail=f"'{filename}' not found !")

    try:
        os.remove(filepath)  # removing file
        return True
    except IsADirectoryError:
        print("The item you want to delete is not a file !")
        raise HTTPException(status_code=404, detail="The item you want to delete is not a file !")
    except PermissionError:
        print("The file cannot be deleted due to permission restrictions !")
        raise HTTPException(status_code=404, detail="The file cannot be deleted due to permission restrictions !")



# main router
fileoperations_router = APIRouter()
fileoperations_router.include_router(downloadfile_router)
fileoperations_router.include_router(infofile_router)
fileoperations_router.include_router(filedelete_router)

