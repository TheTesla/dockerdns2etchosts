# Docker-DNS -> /etc/hosts

This program enables the host to contact the docker containers by their names.

## How it works

This python3 script reads docker container ip addresses and names/aliases from /var/run/docker.sock and copies it to /etc/hosts on the host, where the docker containers are running.

It also deletes the entries from /etc/hosts if the corresponding container is down. 

## Installation

```bash
pip3 install -r requirements.txt
```

## Run

```bash
sudo -E python3 manageetchosts.py 
```

# Author

Stefan Helmert



