
clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

DEBUG_SET_ENV_VARS:= \
	export PORT=8009; \
	export DJANGO_SETTINGS_MODULE=help.settings; \
	export DATABASE_URL=postgres://debug:debug@localhost:5432/help; \
	export SECRET_KEY=DEBUG_SECRET_KEY; \
	export STATICFILES_STORAGE=whitenoise.django.GzipManifestStaticFilesStorage

TEST_SET_ENV_VARS:= \
	export DJANGO_SETTINGS_MODULE=help.settings; \
	export DATABASE_URL=postgres://localhost:5432/help; \
	export SECRET_KEY=TEST_SECRET_KEY; \
	export ZENDESK_URL=zendesk.com; \
	export ZENDESK_USER=test_zendesk_user; \
	export ZENDESK_TOKEN=fake_test_token; \
	export STATICFILES_STORAGE=django.contrib.staticfiles.storage.StaticFilesStorage

build:
	pip3 install -r requirements_test.txt
	$(DEBUG_SET_ENV_VARS) && python manage.py migrate --settings=help.settings.dev
	$(DEBUG_SET_ENV_VARS) && python manage.py collectstatic --noinput --settings=help.settings.dev
	npm install && npm run build

test:
	pep8 . --exclude .venv,node_modules
	npm test
	$(TEST_SET_ENV_VARS) && python manage.py collectstatic --noinput --settings=help.settings.test
	$(TEST_SET_ENV_VARS) && coverage run --source='.' manage.py test --settings=help.settings.test

manage:
	$(TEST_SET_ENV_VARS) && python manage.py $(cmd) --settings=help.settings.test

debug_webserver:
	$(DEBUG_SET_ENV_VARS) && python manage.py collectstatic --settings=help.settings.dev --noinput && ./manage.py runserver 0.0.0.0:$$PORT --settings=help.settings.dev

debug_collectstatic:
	$(DEBUG_SET_ENV_VARS) && python manage.py collectstatic --settings=help.settings.dev


compile_requirements:
	pip-compile requirements.in

upgrade_requirements:
	pip-compile --upgrade requirements.in

compile_test_requirements:
	pip-compile compile requirements_test.in

upgrade_test_requirements:
	pip-compile --upgrade requirements_test.in

compile_all_requirements: compile_requirements compile_test_requirements

upgrade_all_requirements: upgrade_requirements upgrade_test_requirements

test_requirements:
	pip install -r requirements_test.txt
