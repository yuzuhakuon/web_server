import argparse
import subprocess
import os
import psutil

import requests

parser = argparse.ArgumentParser(description="command line parser")
parser.add_argument(
    "command", type=str, help="command type", choices=["start", "stop", "restart", "check"]
)

args = parser.parse_args()


home = os.environ.get("HOME", ".")
local = os.path.join(home, ".local", "var")
pidfile = os.path.join(local, "web_server.pid")


def start():
    print("start")
    subprocess.check_call(["gunicorn -c gunicorn.conf.py app:app"], shell=True)


def stop():
    print("stop")
    subprocess.call([f"kill -9 `cat {pidfile}`"], shell=True)


def restart():
    print("restart")
    stop()
    start()


def update():
    print("update")
    subprocess.check_call(["kill -HUP `cat {pidfile}`"], shell=True)


def check():
    if not os.path.exists(pidfile):
        print(f"no such pid file ({pidfile})")
        return

    pid = 0
    with open(pidfile, "r") as f:
        pid = int(f.read())
    try:
        p = psutil.Process(pid)
        listening = [
            conn for conn in p.connections() if conn.status == psutil.CONN_LISTEN
        ]
        if len(listening) == 0:
            print("nothing listening.")
        for conn in listening:
            url = f"http://localhost:{conn.laddr.port}/index"
            res = requests.get(url, timeout=2)
            print(f"status ok: {res.ok}, status: {res.status_code}, test {url} ")
    except psutil.NoSuchProcess as e:
        print(e)


def main():
    if args.command == "start":
        start()
    elif args.command == "stop":
        stop()
    elif args.command == "restart":
        restart()
    elif args.command == "check":
        check()
    else:
        print("error")


if __name__ == "__main__":
    main()
