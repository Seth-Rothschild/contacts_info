# About

The purpose of this app is for me to learn about Django. The app theoretically stores information about birthdays, addresses, and events for people in my life. It's inspired by [Monica](https://github.com/monicahq/monica) but even when done will have **substantially fewer** features.

## Install
The only dependency is `django`, so you can install that with

```
conda create -p env python=3.10 django
```
and then `conda activate django`. The server runs with `python manage.py runserver`. See the [django documentation](https://docs.djangoproject.com/en/4.0/) for more details.

## License
This is AGPL licensed code. That being said, the vast majority of the code here is boilerplate from django, so if you would like similar functionality and for some reason you're not allowed to use the AGPL license, it likely wouldn't be too difficult to reproduce the steps required to create this.
