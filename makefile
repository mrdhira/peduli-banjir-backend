install:
	pip install -r requirements/base.txt

install-dev:
	pip install -r requirements/development.txt

install-prod:
	pip install -r requirements/production.txt

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

createsuperuser:
	python manage.py createsuperuser

collectstatic:
	python manage.py collectstatic

start:
	gunicorn config.wsgi --preload --bind=0.0.0.0:8000 --workers=${WORKER} --threads=${THREAD} --worker-class=gthread --log-level=debug --chdir=/app

start-dev:
	python manage.py runserver 0.0.0.0:8000

build:
	docker build -t peduli-banjir --build-arg ENV=${ENV} .

start-container:
	docker run -d \
	--restart=always \
	--name peduli-banjir-${CONTAINER_NUMBER} \
	--env-file ${ENV_FILE_PATH} \
	-p 8000:8000 \
	peduli-banjir
