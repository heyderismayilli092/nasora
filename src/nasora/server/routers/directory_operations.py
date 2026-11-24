# Directory Operations
# GET /directory_list
# POST /create_folder
# POST /delete_folder


from fastapi import APIRouter, Form, HTTPException
from nasora.server.utils import config, folder_info
import os

# endpoints
dirlist_router = APIRouter(prefix="/directory_list", tags=["Directory List"])
foldercreate_router = APIRouter(prefix="/create_folder", tags=["Create Folder"])
folderdelete_router = APIRouter(prefix="/delete_folder", tags=["Delete Folder"])
folderinfo_router = APIRouter(prefix="/info_folder", tags=["Folder Informations"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


# directory list
@dirlist_router.get('/')
async def directories():
    dir_list = []
    if not os.path.exists(publishfolder):
        print("The folder you are looking for could not be found !")
        raise HTTPException(status_code=404, detail="The folder you are looking for could not be found !")
    else:
        try:
            for lst in os.listdir(publishfolder):
                dir_list.append(lst)
            return {"directory_list": dir_list}

        except PermissionError:
            print("Folder permissions prevent viewing the content !")
            raise HTTPException(status_code=404, detail="Folder permissions prevent viewing the content !")


# create folder in publish directory
@foldercreate_router.post("")
async def create_folder(
    foldername: str = Form(...)
):
    if not foldername:
        raise HTTPException(status_code=404, detail="Enter a folder name !")

    fullpath = os.path.join(publishfolder, foldername)
    if os.path.exists(fullpath):
        print("This folder is avaliable")
        raise HTTPException(status_code=404, detail="This folder is avaliable")

    try:
        os.makedirs(fullpath)
        return True
    except PermissionError:
        print("Folder permissions are preventing the creation of new folder !")
        raise HTTPException(status_code=404, detail="Folder permissions are preventing the creation of new folder !")


# delete folder in publish directory
@folderdelete_router.post("")
async def delete_folder(
    foldername: str = Form(...)
):
    if not foldername:
        raise HTTPException(status_code=404, detail="Enter a folder name !")

    fullpath = os.path.join(publishfolder, foldername)
    if not os.path.exists(fullpath):
        raise HTTPException(status_code=404, detail="Folder not found !")

    try:
        os.system(f"rm -r {fullpath}")  # remove folder
        return True
    except PermissionError:
        print("Folder permissions are preventing the folder from being deleted !")
        raise HTTPException(status_code=404, detail="Folder permissions are preventing the folder from being deleted !")


# retrieve folder information in publish directory
@folderinfo_router.post("")
async def info_folder(
    path: str = Form(...)
):
    if not path:
        fullpath = os.path.join(publishfolder, ".")

    fullpath = os.path.join(publishfolder, path)
    if not os.path.exists(fullpath):
        raise HTTPException(status_code=404, detail="Folder not found !")

    output = folder_info.get_folder_info(fullpath)
    return output



# main router
diroperations_router = APIRouter()
diroperations_router.include_router(dirlist_router)
diroperations_router.include_router(foldercreate_router)
diroperations_router.include_router(folderdelete_router)
diroperations_router.include_router(folderinfo_router)

