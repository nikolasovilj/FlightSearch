#!/usr/bin/bash


docker-compose up -d
sleep 1

sudo apt install python3-dev libpq-dev
pip install psycopg2


sudo apt install postgresql-client-common
sudo apt install postgresql-client

pip install sqlalchemy pandas Flask requests psycopg2 flask_sqlalchemy
sleep 1
sudo apt install xdg-utils
sleep 1

python3 insert_data.py
sleep 1

echo "password for postgres user king-ict is the same as username -> 'king-ict'"
psql -h localhost -U king-ict -f psql/create_flights.sql

sleep 1
python3 flask-app/app.py &

sleep 3
xdg-open http://localhost:9090
