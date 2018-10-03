#!/usr/bin/env bash

sudo docker-compose exec web python manage.py showmigrations
