# Command Operations
# POST /command


from fastapi import APIRouter, Form, HTTPException
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
        raise HTTPException(status_code=400, detail="Directory not provided !")
    # check command
    if not command:
         raise HTTPException(status_code=400, detail="No command entered !")

    path = os.path.join(publishfolder, directory)  # file full path
    # check folder available
    if not os.path.exists(path):
        print("Path not available !")
         raise HTTPException(status_code=400, detail="Path not available !")

    try:
        # run command
        comm = f"""{command}"""
        output = subprocess.check_output(comm, shell=True, text=True, cwd=path)
        return {"output": output}
    except subprocess.CalledProcessError as e:  # for errors that occur during command execution
        print(f"Error output: {e.stderr}\nError code: {e.returncode}")
        raise HTTPException(status_code=400, detail={"detail": f"Error output {e.stderr}", "errorcode": f"{e.returncode}"},)
    except Exception as e:  # for unexpected errors
        print(f"Error: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {e}")

