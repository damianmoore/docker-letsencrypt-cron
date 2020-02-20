#!/usr/bin/env python
from datetime import datetime
import os
from shutil import copy
import subprocess


RENEWAL_DAYS = 28
cert_dir = '/etc/letsencrypt/live'
cert_copy_dir = '/certs'


def ensure_dh_params():
    dh_params_path = os.path.join(cert_copy_dir, 'dhparams.pem')
    if not os.path.exists(dh_params_path):
        print('Generating DH parameters, 2048 bit long safe prime. This will take a while.')
        subprocess.run(f'openssl dhparam -out {dh_params_path} 2048', shell=True)


def renew_domains():
    failure = False

    for domain in os.environ['DOMAINS'].split(' '):
        cert_path = os.path.join(cert_dir, domain, 'fullchain.pem')
        cert_copy_path = os.path.join(cert_copy_dir, '{}.pem'.format(domain))
        key_path = os.path.join(cert_dir, domain, 'privkey.pem')
        key_copy_path = os.path.join(cert_copy_dir, '{}.key'.format(domain))

        generate = False

        if not os.path.exists(cert_path):
            generate = True
        else:
            expiry_date = subprocess.getoutput(f'openssl x509 -noout -in {cert_path} -dates')
            expiry_date = expiry_date.split('\n')[1].replace('notAfter=', '')
            expiry_date = datetime.strptime(expiry_date, '%b %d %H:%M:%S %Y %Z')
            if (expiry_date - datetime.now()).days <= RENEWAL_DAYS:
                generate = True

        if generate:
            print("Running letsencrypt for {}".format(domain))

            server_param = ''
            if bool(os.environ.get('STAGING', False)):
                server_param = '--staging'

            exit_code, result = subprocess.getstatusoutput(f'certbot \
                --standalone \
                --preferred-challenges http \
                --agree-tos -t \
                --renew-by-default {server_param} \
                --email $EMAIL \
                -d {domain} \
                certonly')
            if exit_code > 0:
                print(result)
                failure = True
            else:
                copy(key_path, key_copy_path)
                copy(cert_path, cert_copy_path)

    if failure:
        exit(1)


if __name__ == '__main__':
    ensure_dh_params()
    renew_domains()
