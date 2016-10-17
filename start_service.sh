#!/bin/bash
PORT=${1:-4180}
cd devenv/register_service
python run.py --port $PORT
cd ../..

if [ "$_WEIZOOM_PRODUCTION" == "1" ]; then
	uwsgi service.ini
else
	python manage.py runserver 0.0.0.0:$PORT
fi
