ifneq (,$(wildcard ./.env))
include .env
export 
ENV_FILE_PARAM = --env-file .env

endif

create_env:
	python3.12 -m venv venv

# act:  # doesn't work
# 	source venv/bin/activate
# realpath venv

mmig: 
	python manage.py makemigrations

mig: 
	python manage.py migrate

serv:
	python manage.py runserver
	
suser:
	python manage.py createsuperuser

cpass:
	python manage.py changepassword

shell:
	python manage.py shell

sapp:
	python manage.py startapp

reqn:
	pip install -r requirements.txt

ureqn:
	pip freeze > requirements.txt

help:  ## makefile documentation.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

lint: ## lint & format
	pre-commit run --all-files

init_db: ## init db
	python manage.py populate_db

# DOCKER COMMANDS
build:
	docker compose -f docker-compose.dev.yml up --build -d --remove-orphans

up:
	docker compose -f docker-compose.dev.yml up -d

down:
	docker compose -f docker-compose.dev.yml down

down-v:
	docker compose -f docker-compose.dev.yml down -v

show-logs:
	docker compose -f docker-compose.dev.yml logs

show-logs-f:
	docker compose -f docker-compose.dev.yml logs -f

redis:
	sudo docker run -it --rm --name redis -p 6378:6379 redis

celery:
	celery -A tech_hive worker -l info --pool=solo

ngrok:
	ngrok http 9000

psql:
	sudo -u postgres psql

dbshell:
	python manage.py dbshell

cpp:
	python manage.py create_premium_plan

clean-media: 
	python manage.py deleteorphanedmedia --noinput=False

clean-static: 
	python manage.py deleteredundantstatic

clean-cloudinary: 
	python manage.py deleteorphanedmedia
	python manage.py deleteredundantstatic

tests:
	python manage.py test

check:
	python manage.py check

check-deploy:
	python manage.py check --deploy 

export_emails:
	python manage.py export_emails > emails.txt

secret-key:
	python manage.py generate_secret_key

show-permissions:
	python manage.py show_permissions

update-permissions:
	python manage.py update_permissions

clear-cache:
	python manage.py clear_cache

notes:
	python manage.py notes

flush-tokens: 
	python manage.py flushexpiredtokens

flush-tokens-verbose:
	python manage.py cleanup_tokens_verbose

