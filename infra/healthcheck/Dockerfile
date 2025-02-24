FROM python:3.10-slim
RUN apt-get update -y && apt-get upgrade -y 
WORKDIR /home/healthcheck
COPY ./app ./
RUN python3.10 -m pip install -r requirements.txt
ENTRYPOINT ["python3.10", "healthcheck.py"]