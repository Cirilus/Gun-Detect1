FROM node:17-alpine

RUN mkdir -p /app
WORKDIR /app

COPY package.json /app/
RUN npm install

COPY ./src /app

CMD ["npm", "start"]