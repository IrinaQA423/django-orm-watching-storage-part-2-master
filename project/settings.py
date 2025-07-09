import os

from environs import env

env.read_env()

DEBUG = env.bool("DEBUG", default=False)

db_engine = env("DB_ENGINE")
db_host = env("DB_HOST")
db_port = env("DB_PORT")
db_name = env("DB_NAME")
db_user = env("DB_USER")
db_password = env("DB_PASSWORD")

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'HOST': db_host,
        'PORT': db_port,
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
    }
}

INSTALLED_APPS = ['datacenter']

SECRET_KEY = env("SECRET_KEY")

ROOT_URLCONF = 'project.urls'

ALLOWED_HOSTS = ['*']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]


USE_L10N = True

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
