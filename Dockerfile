FROM node:4
# ==========================================================
# Docker Image used for Building Gulp based systems
# Usage:
#    docker build -t builder .
#    docker run --rm -v ${PWD}/webapp:/usr/src/app -t builder
#    docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint npm -t builder install
#    docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint bower -t builder install
#    docker run --rm -v ${PWD}/webapp:/usr/src/app -t builder templates
# ==========================================================

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
RUN npm install -g bower gulp

# Build Locally
ENTRYPOINT ["gulp"]

