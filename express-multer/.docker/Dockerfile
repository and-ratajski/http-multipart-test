FROM node:16-alpine AS builder
ARG node_environment=development
ARG upload_dir="/uploads"

RUN mkdir ${upload_dir}
WORKDIR /app

COPY ./app .

ENV NODE_ENV ${node_environment}

RUN yarn