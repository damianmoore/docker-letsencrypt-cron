# docker-letsencrypt-cron
Create and automatically renew website certificates using the Let's Encrypt free CA.

This image will renew your certificates when they have less than 28 days remaining, and place the latest ones in the `/certs` folder on the host.

This repository was forked from [Henri Dwyer's version](https://github.com/henridwyer/docker-letsencrypt-cron) but decides which certificates need renewing based on expiry date rather than doing them all whenever the cron job is run. This lets you manage many more domains without running into [Let's Encrypt's rate limits](https://letsencrypt.org/docs/rate-limits/), as long as you stagger them out. Also, on first run it will generate unique Diffie–Hellman parameters to be used for securing your HTTPS server.

# Setup

In `docker-compose.yml`, change the environment variables:
- Set the `DOMAINS` environment variable to a space separated list of domains for which you want to generate certificates.
- Set the `EMAIL` environment variable for your account on the ACME server, and where you will receive updates from Let's Encrypt.

# ACME Validation challenge

To complete the certification process, you need to prove you are in control of the domain by passing the ACME validation challenge. This requires requests made to `http://YOUR_DOMAIN/.well-known/acme-challenge` be forwarded to this container. Note that your ACME challenge server only runs for the brief few seconds that the request to Let's Encrypt's server is being made, so it can be a bit tricky to test.

## Nginx example

If you use nginx as a reverse proxy, you can add the following to your configuration file in order to pass the ACME challenge.

``` nginx
server {
  listen              80;
  location '/.well-known/acme-challenge' {
    default_type "text/plain";
    proxy_pass http://letsencrypt:80;
  }
}

```

# Usage

```shell
docker-compose up -d
```

When you have your letsencrypt docker container and webserver set up, and if this is a new server, you probably want to run the certificate generation script immediately rather than waiting for the cron job:

```shell
docker exec letsencrypt python /run_letsencrypt.py
```

If you need to debug a problem with your certificate generation process you should be careful not to run into Let's Encrypt's rate limits or you won't be able to try again for a week. You can do this by using their staging server through the use of the environment variable `STAGING`:

```shell
docker exec letsencrypt STAGING=1 python /run_letsencrypt.py
```

At 3AM every day, a cron job will start the script, renewing the certificates that have less than 28 days remaining.

# More information

Find out more about Let's Encrypt: https://letsencrypt.org

Let's Encrypt github: https://github.com/letsencrypt/letsencrypt

SSL config generator for setting up various servers: https://mozilla.github.io/server-side-tls/ssl-config-generator/
