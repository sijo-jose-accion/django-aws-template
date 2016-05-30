FROM node:4.2.6
# ==========================================================
# Docker Image used for Building Gulp based systems
# Usage:
#    docker build -t builder .
#    docker run --rm -v ${PWD}:/usr/src/app -t builder
# ==========================================================

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
RUN npm install -g bower gulp

COPY package.json /usr/src/app/
RUN npm install

# Make directories that will be mounted vide docker -v
RUN mkdir -p /usr/src/app/webapp

# Build Locally
COPY gulpfile.js /usr/src/app/
ENTRYPOINT ["gulp"]
CMD ["base"]