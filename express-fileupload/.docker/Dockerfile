FROM node:16-alpine AS builder
ARG ENVIRONMENT=development
ARG upload_dir="/uploads"

RUN mkdir ${upload_dir}
WORKDIR /app

COPY ./app .

ENV NODE_ENV ${ENVIRONMENT}

RUN yarn