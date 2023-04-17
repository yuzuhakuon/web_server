import os

home = os.environ.get("HOME", ".")
local = os.path.join(home, ".local", "var")
if not os.path.exists(local):
    os.makedirs(local)

port = os.environ.get("WEB_PORT", "8080")

bind = "0.0.0.0:{0}".format(port)
workers = 1
threads = 4
proc_name = "app"
pidfile = os.path.join(local, "web_server.pid")
loglevel = "debug"
logfile = "./logs/debug.log"
errorlog = "./logs/error.log"
# capture_output = True
timeout = 90
daemon = True

worker_class = "gevent"
