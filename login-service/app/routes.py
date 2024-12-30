from ldap3 import Server, Connection, ALL, NTLM, LDAPBindError
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.config import config

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    matrikelnummer = data.get('matrikelnummer')
    password = data.get('password')

    if not matrikelnummer or not password:
        return jsonify({'error': 'Matrikelnummer and password are required'}), 400

    try:
        if authenticate_user(matrikelnummer, password):
            # Get user details (e.g., name, email, role) from LDAP
            user_details = get_user_details_from_ldap(matrikelnummer)  # Implement this function
            access_token = create_access_token(identity=matrikelnummer, additional_claims=user_details)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except LDAPBindError as e:
        return jsonify({'error': 'LDAP bind error: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Authentication failed'}), 500

def authenticate_user(matrikelnummer, password):
    server = Server(config.LDAP_SERVER, port=config.LDAP_PORT, use_ssl=config.LDAP_SSL, get_info=ALL)
    user_dn = config.LDAP_USER_DN.format(matrikelnummer)

    try:
        conn = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)
        return conn.bound
    finally:
        if conn:
            conn.unbind()

def get_user_details_from_ldap(matrikelnummer):
    # Implement logic to retrieve user details (name, email, role) from LDAP
    # ...
    return {
        'name': 'John Doe', 
        'email': 'john.doe@example.com', 
        'role': 'student'
    }

# Example of a protected route
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Hello, {current_user}!'})