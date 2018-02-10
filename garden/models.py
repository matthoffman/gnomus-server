from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username


test_user = User(username="test", password=generate_password_hash("test"))


class Sensor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    # this is where it is _currently_, but note that it can change.
    location_id = db.Column("location_id", db.ForeignKey("location.id"))
    sensor_address = db.Column(db.String(), index=True)
    # sensor_model is something like "DHT22"
    sensor_model = db.Column(db.String())
    # "temperature", "humidity", etc.
    measurement_type = db.Column("measurement_type", db.ForeignKey("measurement_type.id"))


class Location(db.Model):
    """
    Records a single logical "place" that can be measured. It might be a seed bed, a pot, a particular corner of an
    in-ground bed, whatever.
    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())


class MeasurementType(db.Model):
    """
    Reference table for allowed types
    """
    id = db.Column(db.String(), primary_key=True)


# I'm not sure how normalized this table should be. I'm a little worried about changes in sensors or sensor datamodels
# making old readings hard to interpret
class SensorReading(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # do note that the sensor location may change, so we can't only rely on sensor.id for location
    sensor_id = db.Column("sensor_id", db.ForeignKey("sensor.id"))
    location_id = db.Column("location_id", db.ForeignKey("location.id"))
    value = db.Column(db.Float())
    timestamp = db.Column(db.DateTime())
    timestamp_ms = db.Column(db.Integer())
