[![CircleCI](https://circleci.com/gh/uktrade/help.svg?style=svg)](https://circleci.com/gh/uktrade/help)
[![dependencies Status](https://david-dm.org/uktrade/help/status.svg)](https://david-dm.org/uktrade/help)
[![devDependencies Status](https://david-dm.org/uktrade/help/dev-status.svg)](https://david-dm.org/uktrade/help?type=dev)

# help

Department of International Trade Help.  Providing forms for various DIT applications to get feedback and/or provide help to their users.

## First-time setup

Languages/applications needed
- Python 3.5
- Postgres [postgres](https://www.postgresql.org)
- Heroku Toolbelt [heroku](https://toolbelt.heroku.com)


The app runs within a virtual environment. To [install virtualenv](https://virtualenv.readthedocs.org/en/latest/installation.html), run
```shell
    [sudo] pip install virtualenv
```

Install virtualenvwrapper
```shell
    [sudo] pip install virtualenvwrapper
```

Make a virtual environment for this app:
```shell
    mkvirtualenv -p /usr/local/bin/python3.5 help
```

Install dependencies
```shell
    make build
```

## Running the application

Running with django runserver:
```shell
    workon help
    make debug_webserver
```
Then visit [localhost:8000](http://localhost:8000)

Or through heroku:
```shell
    make heroku
```
Then visit [localhost:5000](http://localhost:5000)

## Running tests

Tests include a pep8 style check, django test script and coverage report.

```shell
    workon help
    make test
```
