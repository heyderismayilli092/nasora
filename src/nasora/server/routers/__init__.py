from fastapi import APIRouter

# all routers are being imported
from nasora.server.routers.directory_operations import diroperations_router
from nasora.server.routers.file_operations import fileoperations_router
from nasora.server.routers.command import commrun_router
from nasora.server.routers.upload import upload_router
from nasora.server.routers.serverinfo import serverinfo_router

# main router
api_router = APIRouter()

# the routers here are part of the main api
api_router.include_router(diroperations_router)
api_router.include_router(fileoperations_router)
api_router.include_router(commrun_router)
api_router.include_router(upload_router)
api_router.include_router(serverinfo_router)

