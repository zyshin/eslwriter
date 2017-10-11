# ESLWriter Project
Project home for ESLWriter (http://www.eslwriter.org)

## Install prerequisite python packages

Using `virtualenv` is recommended. Create an fresh environment named `venv` in the project's root folder.

```shell
(venv) pip install -U -r requirements.txt
```

## (Optional) Setup prerequisites for PDF parsing

Only needed if you want to run NLP process on your own computer to build personal corpora.

* Install the latest Java runtime.
* Add [pdftotext](http://www.foolabs.com/xpdf/download.html) to system path (i.e. copy it into `/usr/bin/`).

## Configure Django settings

Download `settings_debug.py` from team Slack and put it into `eslwebsite/`.

**Note: You should NEVER commit `settings_debug.py` or `settings.py` to Github as they contain extreme sensitive data like passwords.**

## Syncdb

```shell
python manage_debug.py migrate
```

## Run server in DEBUG mode

```shell
python manage_debug.py runserver
```

Then have fun searching!

### Run in deploy mode (Not needed during developing)

* The same as DEBUG mode, except that use `settings.py` instead of `settings_debug.py` and run `python manage.py runserver`
