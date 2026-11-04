# Command Operations
# POST /command


from fastapi import APIRouter, Form
from utils import config
import os
import subprocess

# configuration load
loadconf = config.Configuration()
output = loadconf.load()
publishfolder = output["publish-path"]


commrun_router = APIRouter(prefix="/command", tags=["File Download"])

# command run endpoint
@commrun_router.post("")
async def commandrun(
    directory: str = Form(...),
    command: str = Form(...)
):
    # check directory
    if not directory:
        return {"status": False, "details": "Directory not provided !"}
    # check command
    if not command:
        return {"status": False, "details": "Directory not provided !"}

    path = os.path.join(publishfolder, directory)  # file full path
    # check folder available
    if not os.path.exists(path):
        print("Path not available !")
        return {"status": False, "details": "Path not available !"}

    try:
        # run command
        comm = f"""{command}"""
        output = subprocess.check_output(comm, shell=True, text=True, cwd=path)
        return {"status": True, "output": output}
    except subprocess.CalledProcessError as e:  # for errors that occur during command execution
        print(f"Error output: {e.stderr}\nError code: {e.returncode}")
        return {"status": False, "details": f"Error output {e.stderr}", "errorcode": f"{e.returncode}"}
    except Exception as e:  # for unexpected errors
        print(f"Error: {e}")
        return {"status": False, "details": f"Error: {e}"}

