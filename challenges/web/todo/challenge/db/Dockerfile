FROM mongo:6
RUN apt-get update -y  && apt-get upgrade -y
COPY init.js /docker-entrypoint-initdb.d/