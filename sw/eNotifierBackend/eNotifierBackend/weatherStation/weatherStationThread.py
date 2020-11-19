import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from eNotifierBackend.tools.timeTools import getTimeZoneAwareNow, getNow
from eNotifierBackend.weatherStation.weatherStation import WeatherStation


class WeatherStationThread(Thread):

    queue = Queue()
    weatherStation = None

    def __init__(self):
        Thread.__init__(self)
        self.weatherStation = WeatherStation()

    def start(self):
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def run(self):

        interval_minutes = 1

        last_update = getNow() - timedelta(minutes=interval_minutes)

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [db_os_q_msg, db_os_q_data] = self.queue.get()
                if db_os_q_msg == 'quit':
                    run_app=False

            now = getNow()
            next_update = last_update + timedelta(minutes=interval_minutes)
            if now > next_update:
                last_update = now
                self.weatherStation.updateWeatherReport()
                self.weatherStation.updateSensorReport()
                self.weatherStation.updateEpd()

            time.sleep(1)
