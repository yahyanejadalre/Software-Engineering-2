FROM node:16.19.0-alpine

# Install build tools for Node.js
RUN apk add python3 make g++

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY ./package.json ./yarn.lock ./

# yarn install
RUN yarn install

# Bundle app source
ADD . .

# Nuxt.js host address
ENV NUXT_HOST 0.0.0.0

# The Private API Endpoint
ENV BASE_URL http://localhost:8001/api

# The Public API Endpoint
ENV BROWSER_BASE_URL http://localhost:8001/api

# The website main URL
ENV WEBSITE_URL http://localhost:3000

# Build the Nuxt.js project
RUN yarn run build

# Start the server
CMD [ "yarn", "start" ]