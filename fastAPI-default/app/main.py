import logging
import os
import subprocess
import time

from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

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
def upload_test_file(
    background_tasks: BackgroundTasks,
    upload_file: UploadFile = File(
        description="Test file (the bigger the better)",
        alias="uploadFile",
    ),
):
    logger.info("Called `/upload` endpoint, starting work...")
    start_time = time.time()
    save_path = os.path.join("/uploads", upload_file.filename)

    with open(save_path, "wb+") as in_file:
        in_file.write(upload_file.file.read())
    upload_file.file.close()

    end_time = time.time()
    background_tasks.add_task(
        logger.info, f"Work was done in {end_time-start_time} sec."
    )
    background_tasks.add_task(clear_tmp_files)
    # return JSONResponse({"timeElapsed": f"{end_time-start_time}"})
    return FileResponse(
        save_path,
        media_type="application/octet-stream",
    )
