from flask import Flask, request, jsonify, g, render_template
from mysql.connector import connect, Error
from geopy.distance import geodesic

app = Flask(__name__)

DATABASE_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'database': 'airport_db',
    'user': 'root',
    'password': 'Thanuka123po',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'autocommit': True
}

def get_db():
    if 'db' not in g:
        g.db = connect(**DATABASE_CONFIG)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()

@app.route('/')
def index():
    return render_template('P2.html')

@app.teardown_appcontext
def teardown_db(exception):
    close_db()

def calculate_distance(airport1, airport2):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT Latitude, Longitude FROM Airports WHERE AirportID = %s", (airport1,))
        result1 = cursor.fetchone()
        if not result1:
            return None, f"Airport {airport1} not found."
        lat1, lon1 = result1

        cursor.execute("SELECT Latitude, Longitude FROM Airports WHERE AirportID = %s", (airport2,))
        result2 = cursor.fetchone()
        if not result2:
            return None, f"Airport {airport2} not found."
        lat2, lon2 = result2

        distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers
        return distance, None
    except Error as e:
        return None, str(e)

@app.route('/airports', methods=['GET'])
def get_airport_codes():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT AirportID, AirportName FROM Airports")
        airports = cursor.fetchall()
        return jsonify({airport[0]: airport[1] for airport in airports}), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500

@app.route('/distance', methods=['POST'])
def get_distance():
    data = request.json
    if not data or 'airport1' not in data or 'airport2' not in data:
        return jsonify({'error': 'Missing required fields: airport1, airport2'}), 400

    airport1 = data['airport1']
    airport2 = data['airport2']
    distance, error = calculate_distance(airport1, airport2)

    if error:
        return jsonify({'error': error}), 400
    return jsonify({'distance': distance}), 200

@app.route('/quests', methods=['POST'])
def handle_quests():
    data = request.json
    location = data.get('current_location')
    if location == 103:  # Example quest logic
        return jsonify({
            'npc': 'Timur',
            'reward': 150,
            'dialogue': 'Your journey has begun!',
            'next_location': 102
        }), 200
    return jsonify({'message': 'No quest found at this location'}), 404

if __name__ == '__main__':
    app.run(debug=True)
