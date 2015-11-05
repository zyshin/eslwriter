# Introduction
This is the main project base of ESLWriter

## Setup
On linux for example:
* In `eslwebsite/settings.py`, set `DATA_ROOT` to a folder that your apache user (e.g. `www-data: www-data`) can read and write. We will use `data_root` for example.

**Note:** The parent folder of `DATA_ROOT` must be readable and writable by your apache user (e.g. `www-data: www-data`). Change the owner like this:

```shell
sudo chown www-data:www-data parent_to_data_root
```

* The folder structure within DATA_ROOT will be automatically created when running django, by `settings.py`
