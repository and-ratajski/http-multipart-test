import logging
import os
import subprocess
import time
import aiofiles

from fastapi import BackgroundTasks, FastAPI, File, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse

LOG_FILE = "logs/service.log"
logger = logging.getLogger("fastAPI-default")
log_format = logging.Formatter(f"%(asctime)s [%(levelname)s] %(name)s: %(message)s ")
log_handler = logging.FileHandler(LOG_FILE)
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
logger.setLevel("INFO")

app = FastAPI()


def clear_tmp_files() -> None:
    """Clears temporary files"""
    logger.info(f"Clearing temporary files...")
    try:
        subprocess.run(
            [f"rm -rf /app/tmp/*"],
            check=True,
            shell=True,
        )
    except Exception:
        logger.exception("Exception during clearing tmp files.")
    return


@app.get(
    "/",
    summary="Quick file upload form",
    description="Development-only auxiliary endpoint to upload file in a browser.",
    response_class=HTMLResponse,
)
async def upload_form():
    content = """
<body>
<form action="/upload/" 
enctype="multipart/form-data" method="post">
<input name="uploadFile" type="file" multiple>
<input type="submit" value="Upload">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post(
    "/upload",
    summary="Test streaming (multipart) test",
    response_class=FileResponse,
)
async def upload(request: Request):
    try:
        filename = request.headers["filename"]
        save_path = os.path.join("/uploads", filename)
        async with aiofiles.open(save_path, "wb") as f:
            async for chunk in request.stream():
                await f.write(chunk)
    except Exception:
        return {"message": "There was an error uploading the file"}

    return save_path
