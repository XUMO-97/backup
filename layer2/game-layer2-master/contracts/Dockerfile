FROM node:8.11.3-jessie
RUN apt install make

USER node
ENV NPM_CONFIG_PREFIX=/home/node/.npm-global
ENV PATH=$PATH:/home/node/.npm-global/bin

COPY --chown=node . /repo
WORKDIR /repo
RUN npm install
RUN npm run compile

ENTRYPOINT ["make"]