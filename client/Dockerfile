FROM node:10.15-alpine

RUN mkdir -p /app
WORKDIR /app

COPY package.json .
RUN npm i
COPY . .
RUN ["npm", "run", "build"]


FROM nginx:stable-alpine

RUN mkdir -p /usr/share/nginx/html
WORKDIR /usr/share/nginx/html
RUN chmod 777 -R .
RUN chown -R nginx:nginx .

COPY --from=0 /app/dist .
COPY nginx.conf /etc/nginx/nginx.conf