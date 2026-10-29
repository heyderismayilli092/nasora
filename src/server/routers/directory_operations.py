# POST /directory_list/
# Directory listing endpoints scaffold

from fastapi import APIRouter
from utils import config
import os

# endpoints
dirlist_router = APIRouter(prefix="/directory_list", tags=["Directory List"])

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



# main router
diroperations_router = APIRouter()
diroperations_router.include_router(dirlist_router)

