#!/bin/sh
while :
do
    python /run_letsencrypt.py
    sleep 86400
done