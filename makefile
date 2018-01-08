
DEBUG_SET_ENV_VARS:= \
	export DJANGO_SETTINGS_MODULE=help.settings; \
	export DATABASE_URL=postgres://localhost/help; \
	export SECRET_KEY=DEBUG_SECRET_KEY

TEST_SET_ENV_VARS:= \
	$(DEBUG_SET_ENV_VARS); \
	export SECRET_KEY=TEST_SECRET_KEY; \
	export ZENDESK_URL=zendesk.com; \
	export ZENDESK_USER=test_zendesk_user; \
	export ZENDESK_TOKEN=fake_test_token; \

build:
	set -o pipefail
	pip3 install -r requirements_for_test.txt
	# createdb help
	$(DEBUG_SET_ENV_VARS)
	python manage.py migrate
	python manage.py collectstatic --noinput
	npm install && npm run build

test:
	$(TEST_SET_ENV_VARS)
	./scripts/run_tests.sh


debug_webserver:
	source environment.sh && ./manage.py runserver --settings=help.settings.dev

heroku:
	heroku local
