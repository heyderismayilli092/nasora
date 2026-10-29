from fastapi import APIRouter

# all routers are being imported
from .directory_list import router as dirlist_router

# main router
api_router = APIRouter()

# the routers here are part of the main api
api_router.include_router(dirlist_router)

