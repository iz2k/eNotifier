import datetime
import os
import shlex
import shutil
import socket
import subprocess
import sys
import urllib

def getHostname():
    return socket.gethostname()

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getInternetUrllib(url='http://google.com', timeout=3):
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except Exception as e:
        print(e)
        return False

def getInternetCommandLine():
    if (sys.platform == 'win32'):
        ping_cmd = 'ping -n 1 8.8.8.8'
        cmd = subprocess.Popen(ping_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        myStdout = cmd.stdout.read()
        if "TTL=" in str(myStdout):
            return True
        else:
            return False
    else:
        ping_cmd = 'ping -c 1 8.8.8.8'
        cmd = subprocess.Popen(ping_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd.communicate()
        if cmd.returncode == 0:
            return True
        else:
            return False