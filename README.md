# ESLWriter Project
Project home for ESLWriter (http://www.eslwriter.org)

## Install prerequisite python packages

Using `virtualenv` is recommended. Create an fresh environment named `env` in the project's root folder.

```shell
(env) pip install -U -r requirements.txt
```

## (Optional) Setup prerequisites for PDF parsing

Only needed if you want to run NLP process on your own computer to build personal corpora.

* Install the latest Java runtime.
* Add executable `pdftotext` contained in [Xpdf tools](http://www.xpdfreader.com/download.html) to `PATH`.

## Configure Django settings

Download `settings_debug.py` from team Slack and put it into `eslwebsite/`.

**Note: You should NEVER commit `settings_debug.py` or `settings.py` to Github as they contain extreme sensitive data like passwords.**

## Syncdb

```shell
python manage_debug.py migrate
```

## (Optional) Django's [translation framework](https://docs.djangoproject.com/en/dev/topics/i18n/translation/) for multilingual interface

Install [gettext](https://www.gnu.org/software/gettext/) toolset and add `gettext/bin/` to `PATH`

* On Linux, use `apt-get` to install
* On Windows, download [precompiled binaries](https://mlocati.github.io/articles/gettext-iconv-windows.html)

Then compile the translation files for use:

```shell
python manage_debug.py makemessages
```

## Run server in DEBUG mode

```shell
python manage_debug.py runserver
```

Then have fun searching!

### Run in deploy mode (Not needed during developing)

The same as in DEBUG mode, except that use `settings.py` instead of `settings_debug.py` and run `python manage.py runserver`
