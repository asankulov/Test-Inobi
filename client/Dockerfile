FROM node:10.13-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json .
RUN npm i
COPY . .
RUN ["npm", "run", "build"]
