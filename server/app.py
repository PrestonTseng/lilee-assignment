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

url = os.environ.get("DATABASE_URL")
app = Flask(__name__)
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

CREATE_VEHICLE_TABLE = "CREATE TABLE IF NOT EXISTS vehicles (id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name TEXT);"
CREATE_VEHICLE_RETURN_ID = "INSERT INTO vehicles (name) VALUES (%s) RETURNING id;"
LIST_ALL_VEHICLE = "SELECT id, name FROM vehicles;"
UPDATE_VEHICLE = "UPDATE vehicles SET name = %s  WHERE id = %s;"
DELETE_VEHICLE = "DELETE FROM vehicles WHERE id = %s;"

@app.get("/api/vehicles")
def get_vehicles_all():
    connection = psycopg2.connect(url)
    connection.autocommit = True
    with connection.cursor(cursor_factory=RealDictCursor) as cursor:
        try: 
            cursor.execute(CREATE_VEHICLE_TABLE)
            cursor.execute(LIST_ALL_VEHICLE)
            vehicles = cursor.fetchall()
            vehicles.reverse()
            return vehicles
        except Exception as e:
            return e, 500
        finally:
            cursor.close()
            connection.close()
        

@app.post("/api/vehicles")
def add_vehicle():
    data = request.get_json()
    connection = psycopg2.connect(url)
    connection.autocommit = True
    with connection.cursor() as cursor:
        try: 
            cursor.execute(CREATE_VEHICLE_TABLE)
            cursor.execute(CREATE_VEHICLE_RETURN_ID, (data["name"],))
            id = cursor.fetchone()[0]
            return {"id": id, "name": data["name"]}, 200
        except Exception as e:
            return e, 500
        finally:
            cursor.close()
            connection.close()
    

@app.put("/api/vehicles/<id>")
def update_vehicle(id):
    connection = psycopg2.connect(url)
    connection.autocommit = True
    data = request.get_json()

    with connection.cursor() as cursor:
        try:
            cursor.execute(CREATE_VEHICLE_TABLE)
            cursor.execute(UPDATE_VEHICLE, (data["name"], id))
            return {"id": id, "name": data["name"]}, 200
        except Exception as e:
            return e, 500
        finally:
            cursor.close()
            connection.close()
    

@app.delete("/api/vehicles/<id>")
def delete_vehicle(id):
    connection = psycopg2.connect(url)
    connection.autocommit = True

    with connection.cursor() as cursor:
        try: 
            cursor.execute(CREATE_VEHICLE_TABLE)
            cursor.execute(DELETE_VEHICLE, (id,))
            return {"result": True}, 200
        except Exception as e:
            return e, 500
        finally:
            cursor.close()
            connection.close()

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