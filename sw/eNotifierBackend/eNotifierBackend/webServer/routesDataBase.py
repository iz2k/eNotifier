from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from eNotifierBackend.dbManager import Measurement
from eNotifierBackend.dbManager.dbController import dbController
from eNotifierBackend.tools.jsonTools import prettyJson
from eNotifierBackend.weatherStation.weatherStation import WeatherStation


def defineDataBaseRoutes(app : Flask, sio : SocketIO, dbCtl : dbController):

    @app.route('/get-measurements', methods=['POST'])
    def getMeasurements():
        content = flask_request.get_json(silent=True)
        print(content)
        measurements = dbCtl.loadMeasurements(content['startDate'], content['stopDate']).all()
        return prettyJson(measurements)
