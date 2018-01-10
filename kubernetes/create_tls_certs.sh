#!/bin/bash

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /tmp/tls.key -out /tmp/tls.crt -subj "/CN=atpricetracker/O=atpricetracker"
kubectl create secret tls tls-secret --key=/tmp/tls.key --cert=/tmp/tls.crt
