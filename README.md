[![CircleCI](https://circleci.com/gh/uktrade/help.svg?style=shield)](https://circleci.com/gh/uktrade/help)
[![codecov](https://codecov.io/gh/uktrade/help/branch/master/graph/badge.svg)](https://codecov.io/gh/uktrade/help)


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

Create the database
```shell
    createdb help
```

Install dependencies
```shell
    make build
```

## SSO
To make sso work locally add the following to your machine's `/etc/hosts`:

| IP Adress | URL                  |
| --------  | -------------------- |
| 127.0.0.1 | buyer.trade.great    |
| 127.0.0.1 | supplier.trade.great |
| 127.0.0.1 | sso.trade.great      |
| 127.0.0.1 | api.trade.great      |
| 127.0.0.1 | profile.trade.great  |
| 127.0.0.1 | exred.trade.great    |
| 127.0.0.1 | contact.trade.great  |

Then log into `directory-sso` via `sso.trade.great:8001`, and use `help` on `contact.trade.great:8009`

## Running the application

Running with django runserver:
```shell
    workon help
    make debug_webserver
```
Then visit [contact.trade.great:8009](http://contact.trade.great:8009)

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
