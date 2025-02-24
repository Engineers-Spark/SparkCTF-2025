FROM node:16-bullseye-slim

RUN mkdir -p /src

RUN apt-get update \ 
    && apt-get install -y \
    gnupg2 \
    wget \
    curl \
    supervisor

WORKDIR /src
COPY ./src .

RUN  apt-get update \
     && apt-get install -yq libgconf-2-4 \
     && apt-get install -y wget xvfb --no-install-recommends \
     && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
     && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
     && apt-get update \
     && apt-get install -y google-chrome-stable --no-install-recommends \
     && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true

RUN npm install
COPY ./supervisord.conf /etc/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
