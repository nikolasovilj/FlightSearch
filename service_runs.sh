#!/usr/bin/bash

/usr/bin/docker-compose up -d

python3 flask-app/app.py
