from datetime import datetime, timedelta
import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from eNotifierBackend.tools.jsonTools import prettyJson
from eNotifierBackend.tools.osTools import getDiskUsage
from eNotifierBackend.tools.ipTools import getHostname, getIP, getInternetCommandLine
from eNotifierBackend.tools.timeTools import getDateTime


class osInfoThread(Thread):

    queue = Queue()
    sio : SocketIO = None

    def __init__(self):
        Thread.__init__(self)

    def start(self):
        self.emit()
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def run(self):

        last_update = datetime.now()

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [db_os_q_msg, db_os_q_data] = self.queue.get()
                if db_os_q_msg == 'quit':
                    run_app=False

            now = datetime.now()
            next_update = last_update + timedelta(0,10)
            if now > next_update:
                last_update = now
                self.emit()

            time.sleep(0.1)

    def emit(self):
        self.sio.emit('osInfo', prettyJson(getReport()))

def getReport():
    # Get hostname and IP
    hostname = getHostname()
    ip = getIP()

    # Get internet connection status
    internet = getInternetCommandLine()

    # Get FS space
    [total_GB, free_GB] = getDiskUsage()

    # Get TimeZone
    datetime = getDateTime()

    hostinfo =  {
        'hostname' : hostname,
        'ip' : ip,
        'internet' : internet,
        'fs_total_GB' : total_GB,
        'fs_free_GB' : free_GB,
        'datetime' : datetime
    }
    return hostinfo
