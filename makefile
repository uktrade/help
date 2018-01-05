build:
	./scripts/bootstrap.sh

test:
	./scripts/run_tests.sh

local_env:
	echo "
	export DJANGO_SETTINGS_MODULE='help.settings'
	export DATABASE_URL='postgres://localhost/help'
	export SECRET_KEY='REPLACE ME WITH AN ACTUAL SECRET KEY'
	"> environment.sh

debug_webserver:
	source environment.sh && ./manage.py runserver --settings=help.settings.dev

heroku:
	heroku local
