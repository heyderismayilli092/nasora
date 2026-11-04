from fastapi import APIRouter

# all routers are being imported
from .directory_operations import diroperations_router
from .file_operations import fileoperations_router
from .command import commrun_router
from .upload import upload_router

# main router
api_router = APIRouter()

# the routers here are part of the main api
api_router.include_router(diroperations_router)
api_router.include_router(fileoperations_router)
api_router.include_router(commrun_router)
api_router.include_router(upload_router)

