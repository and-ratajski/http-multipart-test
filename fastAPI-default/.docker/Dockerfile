FROM python:3.10-bullseye AS base
ARG upload_dir="/uploads"

RUN mkdir ${upload_dir}
WORKDIR /app

COPY ./.docker/requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]