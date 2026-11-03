# nasora
# 0.0.1

from fastapi import FastAPI
from utils import config
from routers import api_router
import sys

title='nasora'
version='0.0.1'
description='A lightweight FastAPI-based NAS file management API with a Python SDK for remote file transfers and storage operations'
app = FastAPI(
    title=title,
    version=version,
    description=description,
)
app.include_router(api_router)


# check configuration
configcheck = config.Configuration()
checkoutput = configcheck.checkconf()
if checkoutput["status"] == False:
    print(checkoutput["details"])
    sys.exit(1)


@app.get('/')
def index():
    return {'app': title, 'version': version, 'description': description}

