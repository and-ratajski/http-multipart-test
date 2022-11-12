import logging
import os
import subprocess
import time

from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse

LOG_FILE = "logs/service.log"
logger = logging.getLogger("fastAPI")
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
<form action="/test/" 
enctype="multipart/form-data" method="post">
<input name="uploadFile" type="file" multiple>
<input type="submit" value="Upload">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post(
    "/test",
    summary="Test streaming (multipart) test",
    response_class=FileResponse,
)
async def upload_tes_file(
    background_tasks: BackgroundTasks,
    upload_file: UploadFile = File(
        description="Test file (the bigger the better)",
        alias="uploadFile",
    ),
):
    logger.info("Called `/test` endpoint, starting work...")
    start_time = time.time()
    save_path = os.path.join("/app/tmp", upload_file.filename)

    with open(save_path, "wb+") as in_file:
        in_file.write(upload_file.file.read())

    end_time = time.time()
    background_tasks.add_task(
        logger.info, f"Work was done in {end_time-start_time} sec."
    )
    background_tasks.add_task(clear_tmp_files)
    return save_path
