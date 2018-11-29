#UTF-8
import os
import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

preload_app = True
debug = True
loglevel = 'info'
bind = '0.0.0.0:6990'
pidfile = '/home/work/ChatRobot/server/logs/gunicorn.pid'
logfile = '/home/work/ChatRobot/server/logs/debug.log'

accesslog = '/home/work/ChatRobot/server/logs/debug.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = '/home/work/ChatRobot/server/logs/debug.log'

workers = multiprocessing.cpu_count() * 4 + 1
threads = multiprocessing.cpu_count() * 4
worker_class = 'gevent'

x_forwarded_for_header = 'X-FORWARDED-FOR'
