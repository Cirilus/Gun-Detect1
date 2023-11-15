FROM node:17-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN npm i

COPY . /app

CMD ["npm", "start"]