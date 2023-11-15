FROM node:17-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN npm i

COPY ./src /app

CMD ["npm", "start"]