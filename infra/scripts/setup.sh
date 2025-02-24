#! /bin/bash

sudo apt update -y && sudo apt upgrade -y

sudo apt-get install -y \
    apt-transport-https -y \
    ca-certificates -y \
    curl -y \
    gnupg-agent -y \
    software-properties-common -y


#### docker / docker compose ####

sudo apt-get update && sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88 | grep docker@docker.com || exit 1
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin -y

#### ctfcli, discord-webhook ####
sudo apt install python3-pip
python3 -m pip install git+https://github.com/CTFd/ctfcli.git
python3 -m pip install git+https://github.com/lovvskillz/python-discord-webhook

