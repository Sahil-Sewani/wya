from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_bcrypt import check_password_hash, generate_password_hash
import pymysql

app = Flask(__name__)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])  # Enable CORS for all routes
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Replace with your secret key

jwt = JWTManager(app)

# Database Configuration
connection = pymysql.connect(
    host='sql5.freesqldatabase.com',
    database='sql5672639',
    user='sql5672639',
    password='eYYYvQuXZC'
)

# User Model
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

'''
# the one that works
# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        cursor.execute('INSERT INTO User (username, password) VALUES (%s, %s)', (username, password))
        connection.commit()

    return jsonify({'message': 'User created successfully'}), 201
'''

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = generate_password_hash(password).decode('utf-8')  # Hash the password
        cursor.execute('INSERT INTO User (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Get All Users
@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User')
        users = cursor.fetchall()
        if not users:
            return jsonify({'message': 'No users found'}), 404

        users_list = [{
            'id': user[0],  # Assuming the 'id' is the first column
            'username': user[1]  # Assuming the 'username' is the second column
            # Add more user details if needed
        } for user in users]

        return jsonify(users_list), 200

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User WHERE username = %s', (username,))
        user = cursor.fetchone()
        if user:
            stored_password_index = None
            # Find the index of the column named like a password (case-insensitive)
            for idx, column_name in enumerate(cursor.description):
                if 'password' in column_name[0].lower():
                    stored_password_index = idx
                    break

            if stored_password_index is not None:
                stored_password = user[stored_password_index]
                if check_password_hash(stored_password, password):
                    return jsonify({'message': 'Login successful'}), 200
                    # return jsonify({'access_token': access_token}), 200 # access token code for verifying user ID upon login
                else:
                    return jsonify({'message': 'Invalid password'}), 401
            else:
                return jsonify({'message': 'Password column not found'}), 500
        else:
            return jsonify({'message': 'User does not exist'}), 404
'''
# Add Package (Requires JWT)
@app.route('/add_package', methods=['POST'])
@jwt_required()
def add_package():
    current_user = get_jwt_identity()
    data = request.get_json()
    package_name = data.get('package_name')
    tracking_number = data.get('tracking_number')

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User WHERE username = %s', (current_user,))
        user = cursor.fetchone()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        cursor.execute('INSERT INTO Package (package_name, tracking_number, user_id) VALUES (%s, %s, %s)',
                       (package_name, tracking_number, user['id']))
        connection.commit()

    return jsonify({'message': 'Package added successfully'}), 200
'''
# Add Package (Requires User Authentication)
@app.route('/add_package', methods=['POST'])
def add_package():
    data = request.get_json()
    package_name = data.get('package_name')
    tracking_number = data.get('tracking_number')
    user_id = data.get('user_id')  # Retrieve user_id from the request (either from authentication or session)

    # Perform the addition to the Package table
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO Package (package_name, tracking_number, user_id) VALUES (%s, %s, %s)',
                       (package_name, tracking_number, user_id))
        connection.commit()

    return jsonify({'message': 'Package added successfully'}), 200

# Get User's Packages (Requires JWT)
@app.route('/get_packages', methods=['GET'])
@jwt_required()
def get_packages():
    current_user = get_jwt_identity()

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM User WHERE username = %s', (current_user,))
        user = cursor.fetchone()
        if not user:
            return jsonify([]), 200

        cursor.execute('SELECT * FROM Package WHERE user_id = %s', (user['id'],))
        packages = cursor.fetchall()
        packages_list = [{'package_name': package['package_name'], 'tracking_number': package['tracking_number']} for package in packages]

        return jsonify(packages_list), 200

if __name__ == '__main__':
    app.run(debug=True)

