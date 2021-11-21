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
	gunicorn config.wsgi --bind=0.0.0.0:8000 --workers=2 --threads=2 --worker-class=gthread --log-level=debug --worker-tmp-dir=/dev/shm --chdir=/app

start-dev:
	python manage.py runserver 0.0.0.0:8000


