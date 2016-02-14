# Introduction
This is the main project base of ESLWriter

## Prerequisites
* See the [query project](https://github.com/zyshin/query)
* Install Java runtime
* Add [pdftotext](http://www.foolabs.com/xpdf/download.html) to system path (i.e. copy it into `/usr/bin/`).

## Setup
On linux for example:

* In `eslwebsite/settings.py`, set `DATA_ROOT` to a folder that your apache user (e.g. `www-data: www-data`) can read and write. We will use `data_root` for example.

**Note:** The parent folder of `DATA_ROOT` must be readable and writable by your apache user (e.g. `www-data: www-data`). Change the owner like this:

```shell
sudo chown www-data:www-data parent_to_data_root
```

* TODO: The folder structure within DATA_ROOT will be automatically created in the deploy stage before running django, by `deploy.py`.
