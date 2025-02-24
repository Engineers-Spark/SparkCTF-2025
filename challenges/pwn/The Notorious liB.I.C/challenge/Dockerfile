FROM ubuntu:18.04 as chroot

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --no-create-home -u 2000 user

COPY main /app/run
COPY flag.txt /app/flag.txt
COPY ld-linux-x86-64.so.2 /app/ld-linux-x86-64.so.2
COPY libc.so.6 /app/libc.so.6

FROM pwn.red/jail

COPY --from=chroot / /srv
ENV JAIL_POW=0 JAIL_PORT=1337

WORKDIR /srv/app
RUN chmod +x ld-linux-x86-64.so.2
RUN chmod +x libc.so.6
RUN chmod +x run
