FROM node:17-alpine

WORKDIR /app

COPY package.json /app/package.json

RUN npm install --only=prod

COPY . /app

CMD ["npm", "start"]