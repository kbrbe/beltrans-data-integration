# Database

This folder contains dockerized software to start a Blazegraph RDF database with a reverse proxy to handle authentication.
Using Letsencrypt the reverse proxy uses HTTPS for a secure connection.
The setup is configured via environment variables (see `example.env`).


## Steps to install 

The database can be started with the following **three steps**.

1. Configure the setup

1.1. set required environment variables

```bash
cp example.env .env

# provide values for the variables in .env using your favorite text editor
```

1.2. generate user and passwords for the NGINX reverse proxy

```bash
# install tool if needed
sudo apt-get install apache2-utils

# generate a user by providing a username (you will be prompoted to set a password)
htpasswd -n <user_name>

# add the resulting line consisting of username and password hash to the file ./data/nginx/conf.d/.htpasswd
``` 


**The use of Letsencrypt currently does not work**
~~2. Initialize SSL certificates (start with a dummy certifiate such that nginx can start and then generate a real Letsencrypt certificate)
Some of the environment variables are already used so they need to be exported.~~

```bash
# export environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

# set up SSL via LetsEncrypt
bash init-letsencrypt.sh
```

3. Start the docker containers

```bash
docker-compose up
```

## FAQ

### permission denied when starting Blazegraph

Blazegraph uses a journal file to store data, by default this file is called `bigdata.jnl`.
In our setup this file will be mounted from `data/blazegraph/` into the docker container such that it also persists when the container is shutdown.

However, the user and group ID of the host user and the Blazegraph user in the docker container have to match.
Therefore the corresponding variables in `blazegraph/Dockerfile` need to be updated (and the container needs to be rebuilt with `docker-compose build blazegraph`.

**todo: use environment variables from .env**

## Acknowledgement

The setup is based on several online sources

* Blazegraph Dockerfile based on: https://github.com/viaacode/knowledge-graph-organizations
* Setting up reverse proxy rules for nginx and Blazegraph https://baskauf.blogspot.com/2017/07/how-and-why-we-set-up-sparql-endpoint.html
* Setting up an nginx docker container with Letsencrypt https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
