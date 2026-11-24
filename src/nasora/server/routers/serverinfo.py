# Server Informations
# POST /serverinfo


from fastapi import APIRouter, Form, HTTPException
from nasora.server.utils import config
import os
import subprocess

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]
server_name = output["server-name"]


server_info = APIRouter(prefix="/serverinfo", tags=["Server Informations"])

# server informations
@server_info.get("")
async def serverinfo():
    try:
        return {
            "server_name": server_name,
            "publish_path": publishfolder
        }
    except Exception as e:  # for unexpected errors
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")


# main router
serverinfo_router = APIRouter()
serverinfo_router.include_router(server_info)

