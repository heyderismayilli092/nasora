# Directory Operations
# GET /directory_list
# POST /create_folder


from fastapi import APIRouter, Form
from utils import config
import os

# endpoints
dirlist_router = APIRouter(prefix="/directory_list", tags=["Directory List"])
foldercreate_router = APIRouter(prefix="/create_folder", tags=["Create Folder"])

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
        return {"status": False, "details": "The folder you are looking for could not be found !"}
    else:
        try:
            for lst in os.listdir(publishfolder):
                dir_list.append(lst)
            return {"directory_list": dir_list}

        except PermissionError:
            print("Folder permissions prevent viewing the content !")
            return {"status": False, "details": "Folder permissions prevent viewing the content !"}


# create folder in publish directory
@foldercreate_router.post("")
async def create_folder(
    foldername: str = Form(...)
):
    if not foldername:
        return {"status": False, "details": "Enter a folder name !"}

    fullpath = os.path.join(publishfolder, foldername)
    if os.path.exists(fullpath):
        return {"status": False, "details": "This folder is avaliable"}

    try:
        os.makedirs(fullpath)
        return {"status": True}
    except PermissionError:
        print("Folder permissions are preventing the creation of new folder !")
        return {"status": False, "details": "Folder permissions are preventing the creation of new folder !"}



# main router
diroperations_router = APIRouter()
diroperations_router.include_router(dirlist_router)
diroperations_router.include_router(foldercreate_router)

