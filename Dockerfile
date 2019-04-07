FROM certbot/certbot

RUN mkdir /certs

COPY ./scripts/ /

ENTRYPOINT ["/bin/sh", "-c"]

CMD ["/run_cron.sh"]
