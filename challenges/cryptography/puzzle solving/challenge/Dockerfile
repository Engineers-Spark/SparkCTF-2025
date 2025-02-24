FROM python:3.9-slim-buster 

RUN apt update -y && apt upgrade -y

RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf/app
COPY ./app .

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m pip install gunicorn

RUN python3 -m venv .venv
RUN . .venv/bin/activate

RUN chown -R root:ctf /home/ctf/
RUN chown -R root:ctf /home/ctf/app/templates
RUN chown root:ctf /home/ctf/app/app.py
RUN chown root:ctf /home/ctf/app/secret.py
RUN chmod +x ./start.sh

USER ctf

ENTRYPOINT ./start.sh

