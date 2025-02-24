

FROM python:3.9-slim-buster

RUN apt-get update && apt-get -y upgrade

RUN groupadd -r ctf && useradd -r -g ctf ctf
COPY task.py /home/ctf/
COPY launch.sh /home/ctf/
COPY ynetd /home/ctf/
COPY secret.py /home/ctf

RUN chown -R root:ctf /home/
RUN chmod 750 /home/ctf/task.py
RUN chmod 750 /home/ctf/ynetd
RUN chmod 750 /home/ctf/launch.sh
RUN chmod 750 /home/ctf/secret.py
