#!/usr/bin/env bash

#other migrate commands available too
#https://docs.djangoproject.com/en/2.1/topics/migrations/

sudo docker-compose exec web python manage.py makemigrations
