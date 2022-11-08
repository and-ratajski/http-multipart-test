FROM node:16-alpine AS builder

WORKDIR /app

COPY ./app .

ENV NODE_ENV development

RUN yarn