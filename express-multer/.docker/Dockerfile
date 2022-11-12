FROM node:16-alpine AS builder
ARG node_environment=development

RUN mkdir /uploads
WORKDIR /app

COPY ./app .

ENV NODE_ENV ${node_environment}

RUN yarn