# POST /directory_list/
# Directory listing endpoints scaffold

from fastapi import APIRouter
from utils import config

router = APIRouter()

@route.get('/directory_list/')
async def directories(
    directory: str = Form(...)
):
    dir_list = []
    if not os.path.exists(directory):
        return {"status": False, "details": "The folder you are looking for could not be found!"}
    else:
        for lst in os.listdir(directory):
            dir_list.append(lst)
        return {"directory_list": dir_list}

