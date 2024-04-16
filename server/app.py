from asyncio import Event
import json
import random
from flask_socketio import SocketIO
import time
from flask import Flask, request
from psycopg2.extras import RealDictCursor
import psycopg2
import os
from flask_cors import CORS
from threading import Thread, Event
from flask_sqlalchemy import SQLAlchemy
from controller import blue_vehicle
from model import db

url = os.environ.get("DATABASE_URL")
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = url

app.register_blueprint(blue_vehicle, url_prefix='/api/vehicles')

db.init_app(app)

with app.app_context():
    db.create_all()

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

thread = Thread()
thread_stop_event = Event()
simulation_vehicle_id = []

def speed_simulation():
    global simulation_vehicle_id
    while (not thread_stop_event.isSet()) and len(simulation_vehicle_id) > 0:
        for id in simulation_vehicle_id:
            socketio.emit('speed', {"id": id, "speed": random.randint(0, 100)})
        socketio.sleep(1)

@socketio.on('monitor_start')
def monitor_speed(id):
    global simulation_vehicle_id
    if id not in simulation_vehicle_id:
        simulation_vehicle_id.append(id)
    global thread
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(speed_simulation)
    
@socketio.on('monitor_end')
def monitor_speed(id):
    global simulation_vehicle_id
    if id in simulation_vehicle_id:
        simulation_vehicle_id.remove(id)

if __name__ == '__main__':
    socketio.run(app, debug=True)