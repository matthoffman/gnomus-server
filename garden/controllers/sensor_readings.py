import uuid
import datetime
import collections
from logging import getLogger
from json import dumps
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from garden.extensions import cache
from garden.forms import LoginForm
from garden.models import User, db, Sensor, SensorReading

readings = Blueprint('readings', __name__)
logger = getLogger(__name__)
readingLogger = getLogger("readings")


@readings.route("/reading", methods=["POST"])
def new_reading():
    reading = request.get_json(force=True, cache=False)
    # this might look something like:
    # {"id": "abc123",
    #  "readings": {
    #    "moisture": {"adc.1": 0.23},
    #    "temperature": {"adc.2": 0.31,
    #                    "adc.3": 0.20}
    #    }
    #  }
    #
    # or maybe:
    # {"id": "abc123",
    #  "readings": {"abc123.adc.1": {"value": 0.23},
    #               "abc123.adc.2": {"value": 0.31},
    #               "abc123.adc.3": {"value": 334},
    #               "abc123.0x76": {"value": 432}
    #               }
    #  }
    #
    # We want to turn it into a set of SensorReading records like:
    # { "id": ...,
    #   "sensor_id" : looked_up_sensor_id,
    #   "location_id": looked_up_location_id,
    #   "value": 0.23,
    #   "timestamp": ...
    # }
    #
    # So, for each reading in this payload...
    readingLogger.info(dumps(reading))

    frm = reading["id"]
    logger.info("Got reading from {}".format(frm))

    now = datetime.datetime.now()
    now_formatted = now.isoformat()
    now_millis = now.timestamp()
    for sensor_type in reading["readings"].keys():
        by_type = reading["readings"][sensor_type]
        for sensor_address in by_type.keys():
            value = by_type[sensor_address]
            if isinstance(v, collections.Mapping):
                value = value["value"]

            sensor = db.select("select * from sensor where sensor_address = {}", sensor_address)
            sr = SensorReading()
            sr["id"] = uuid.uuid4()
            if sensor:
                sr["sensor_id"] = sensor.id
                sr["location_id"] = sensor.location_id

            sr["sensor_type"] = sensor_type
            sr["value"] = value
            sr["timestamp"] = now_formatted
            sr["timestamp_ms"] = now_millis
            db.insert(sr)
