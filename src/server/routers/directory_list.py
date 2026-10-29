# POST /directory_list/
# Directory listing endpoints scaffold

from fastapi import APIRouter
from utils import config
import os

router = APIRouter(prefix="/directory_list", tags=["Kullanıcılar"])

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]

@router.get('/')
async def directories():
    dir_list = []
    if not os.path.exists(publishfolder):
        return {"status": False, "details": "The folder you are looking for could not be found!"}
    else:
        for lst in os.listdir(publishfolder):
            dir_list.append(lst)
        return {"directory_list": dir_list}

