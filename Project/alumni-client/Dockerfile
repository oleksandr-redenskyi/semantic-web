FROM node:20.11.1

ENV NODE_ENV=production
ARG PROJECT_NAME
ARG STAGE

WORKDIR /app
COPY package.json /app/package.json
# When NODE_ENV=production, npm omits dev dependencies by default
RUN npm install

COPY . /app
RUN npm run build

CMD [ "npm", "start"]
