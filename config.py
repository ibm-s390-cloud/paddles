# This is a sample configuration file.
#
# Modify it to fit your environment and rename it to something like 'prod.py'

import os
import sentry_sdk
from paddles.hooks import IsolatedTransactionHook, SentryHook
from paddles import models
from paddles.hooks.cors import CorsHook

sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        sentry_dsn,
        traces_sample_rate=1,
    )

# Server Specific Configurations
server = {
    'port': os.environ.get('PADDLES_SERVER_PORT', '8080'),
    'host': os.environ.get('PADDLES_SERVER_HOST', '172.23.232.4')
}

# statsd = {
#     'host': os.environ.get('PADDLES_STATSD_HOST', 'example.com'),
#     'prefix': os.environ.get('PADDLES_STATSD_PREFIX', 'ceph.test.teuthology.your_lab'),
# }
statsd = {
    'host': 'm1306004.lnxero1.boe',
    'prefix': 'ceph.test.teuthology.ibmz_lab',
}

# # These values will be specific to your site
# address = os.environ.get(
#     'PADDLES_ADDRESS',
#     'http://paddles.front.sepia.ceph.com'
# )
# job_log_href_templ = os.environ.get(
#     'PADDLES_JOB_LOG_HREF_TEMPL',
#     'http://qa-proxy.ceph.com/teuthology/{run_name}/{job_id}/teuthology.log'
# )
address = 'http://m1306004.lnxero1.boe'
job_log_href_templ = 'http://172.23.232.4/{run_name}/{job_id}/teuthology.log'  # noqa
default_latest_runs_count = 25

# Pecan Application Configurations
app = {
    'root': 'paddles.controllers.root.RootController',
    'modules': ['paddles'],
    #'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/paddles/templates',
    'default_renderer': 'json',
    'guess_content_type_from_ext': False,
    'debug': False,
    'hooks': [
        IsolatedTransactionHook(
            models.start,
            models.start_read_only,
            models.commit,
            models.rollback,
            models.clear
        ),
        # Uncomment this if you want more logging
        #RequestViewerHook({'blacklist': ['/favicon.ico', '/errors/'],
        #                   'items':
        #                  ['date', 'path', 'status', 'method', 'controller'],
        #                   }),
        CorsHook(),
        SentryHook(),
    ],
}

logging = {
    'disable_existing_loggers': False,
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'paddles': {'level': 'DEBUG', 'handlers': ['console']},
        'sqlalchemy': {'level': 'WARN', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       ' %(message)s')
        }
    }
}

def get_sqlalchemy_url():
    import subprocess
    return subprocess.getoutput("pecan get_secret")

sqlalchemy = {
    # 'url': get_sqlalchemy_url(),
    'url': os.environ.get('PADDLES_SQLALCHEMY_URL', 'postgresql+psycopg2://paddles:pass4root@127.0.0.1/paddles'),
    # Uncomment to see SQL queries in logs
    #'echo':          True,
    #'echo_pool':     True,
    'pool_recycle':  3600,
    'encoding':      'utf-8',
    'isolation_level': 'SERIALIZABLE', # required for correct job reporting
}
