from fastapi import APIRouter

# all routers are being imported
from .directory_operations import diroperations_router
from .file_operations import fileoperations_router

# main router
api_router = APIRouter()

# the routers here are part of the main api
api_router.include_router(diroperations_router)
api_router.include_router(fileoperations_router)

