from .base import *             # NOQA
import sys
import logging.config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS'].update({'debug': True})

STATIC_URL = '/static/'
STATIC_ROOT = '/www/static/'
STATICFILES_DIRS = (
    ('dist', os.path.join(STATIC_ROOT, 'dist')),
)

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
if "celery" in sys.argv[0]:
    DEBUG = False

# Show emails to console in DEBUG mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Show thumbnail generation errors
THUMBNAIL_DEBUG = True

# Log everything to the logs directory at the top
LOGFILE_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'logs')

# Reset logging
# (see http://www.caktusgroup.com/blog/2015/01/27/Django-Logging-Configuration-logging_config-default-settings-logger/)

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGFILE_ROOT, 'project.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)

# Debug Toolbar (http://django-debug-toolbar.readthedocs.org/)
INSTALLED_APPS += ('debug_toolbar',)
DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1', '192.168.99.100',)
DEBUG_TOOLBAR_PANELS = [
 'debug_toolbar.panels.versions.VersionsPanel',
 'debug_toolbar.panels.timer.TimerPanel',
 'debug_toolbar.panels.settings.SettingsPanel',
 'debug_toolbar.panels.headers.HeadersPanel',
 'debug_toolbar.panels.request.RequestPanel',
 'debug_toolbar.panels.sql.SQLPanel',
 # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
 'debug_toolbar.panels.templates.TemplatesPanel',
 'debug_toolbar.panels.signals.SignalsPanel',
 'debug_toolbar.panels.logging.LoggingPanel',
 'debug_toolbar.panels.redirects.RedirectsPanel',
]

