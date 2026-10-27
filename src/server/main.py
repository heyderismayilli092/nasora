# nasora
# 0.0.1

from fastapi import FastAPI
from utils import config

app = FastAPI(
    title="Nasora",
    version="0.0.1",
    description="A lightweight FastAPI-based NAS file management API with a Python SDK for remote file transfers and storage operations",
)

