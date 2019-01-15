#!/usr/bin/env bash
cd rcp-rest-api/
git pull
docker-compose build && docker-compose down && docker-compose up -d
docker-compose run -d rcp_django python3 manage.py qcluster