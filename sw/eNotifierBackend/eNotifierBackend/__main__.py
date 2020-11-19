#!/usr/bin/env python3
import argparse
import time

from eNotifierBackend.bme680.simpleBme680 import SimpleBME680
from eNotifierBackend.osInfo.osInfoThread import osInfoThread
from eNotifierBackend.sgp30.simpleSgp30 import SimpleSGP30
from eNotifierBackend.weatherStation.weatherStationThread import WeatherStationThread
from eNotifierBackend.webServer.webServer import webServerThread


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-clock controller.")

    parser.add_argument("-port", default='8081', help=" port used for web server")

    args = parser.parse_args()

    # Define threads
    webserverTh = webServerThread(log=False)
    osInfoTh = osInfoThread()
    weatherStationThread = WeatherStationThread()

    webserverTh.define_webroutes(weatherStationThread.weatherStation)

    # Pass SIO to threads
    osInfoTh.set_sio(webserverTh.sio)

    try:
        # Start threads
        osInfoTh.start()
        weatherStationThread.start()
        webserverTh.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        webserverTh.join()

        # When server ends, stop threads
        osInfoTh.stop()
        weatherStationThread.stop()

        # Print Goodby msg
        print('Exiting R102-DB-CTL...')

    except KeyboardInterrupt:
        # Stop threads
        osInfoTh.stop()
        weatherStationThread.stop()


# If executed as main, call main
if __name__ == "__main__":
    main()
