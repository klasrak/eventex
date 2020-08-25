from eventex.settings import *

EVENTEX_APPS = [
    "test_without_migrations",
    "eventex.core",
    "eventex.subscriptions",
]

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
] + EVENTEX_APPS

# TEST_WITHOUT_MIGRATIONS_COMMAND = "django_nose.management.commands.test.Command"
