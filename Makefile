build:
	docker run --name redis_sl -p 6379:6379 -d redis

run:
	docker start redis_sl
	gunicorn --config gunicorn_config.py main:app