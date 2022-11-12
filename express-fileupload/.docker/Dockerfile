FROM node:16-alpine AS builder
ARG ENVIRONMENT=development

WORKDIR /app

COPY ./app .

ENV NODE_ENV ${ENVIRONMENT}

RUN yarn