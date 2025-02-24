FROM python:3.12.8-slim-bookworm

RUN apt-get update && apt-get -y upgrade

RUN groupadd -r ctf && useradd -r -g ctf ctf
COPY challenge.py /home/ctf/
COPY launch.sh /home/ctf/
COPY ynetd /home/ctf/
RUN chown -R root:ctf /home/ctf
RUN chmod 750 /home/ctf/challenge.py
RUN chmod 750 /home/ctf/ynetd
RUN chmod 750 /home/ctf/launch.sh

USER ctf
EXPOSE 6001

CMD /home/ctf/ynetd -p 6001 /home/ctf/launch.sh
