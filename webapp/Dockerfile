FROM node:5
# ==========================================================
# Docker Image used for Building Gulp based systems
# Usage:
# docker build -t my_proj/builder webapp
# docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint npm -t my_proj/builder install
# docker run --rm -v ${PWD}/webapp:/usr/src/app --entrypoint bower -t my_proj/builder --allow-root --config.interactive=false install
# docker run --rm -v ${PWD}:/usr/src/app -t my_proj/builder templates
==========================================================

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app dependencies
RUN npm install -g bower gulp-cli

# Build Locally
WORKDIR /usr/src/app/webapp
ENTRYPOINT ["gulp"]


