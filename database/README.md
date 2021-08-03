# Database

This folder contains dockerized software to start a Blazegraph RDF database with a reverse proxy to handle authentication.
Using Letsencrypt the reverse proxy uses HTTPS for a secure connection.
The setup is configured via environment variables (see `example.env`).


## Steps to install 

The database can be started with the following **three steps**.

1. Configure the setup by setting required environment variables

```bash
cp example.env .env

# provide values for the variables in .env using your favorite text editor
```

2. Initialize SSL certificates (start with a dummy certifiate such that nginx can start and then generate a real Letsencrypt certificate)
Some of the environment variables are already used so they need to be exported.

```bash
# export environment variables
export $(cat .env | sed 's/#.*//g' | xargs)

# set up SSL via LetsEncrypt
bash letsencrypt.sh
```

3. Start the docker containers

```bash
docker-compose up
```


## Acknowledgement

The setup is based on several online sources

* Blazegraph Dockerfile based on: github.com/viaacode/knowledge-graph-organizations
* Setting up reverse proxy rules for nginx and Blazegraph baskauf.blogspot.com/2017/07/how-and-why-we-set-up-sparql-endpoint.html
* Setting up an nginx docker container with Letsencrypt pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
