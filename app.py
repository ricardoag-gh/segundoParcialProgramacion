import sqlite3
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
app = Flask(__name__)

#Secret key to use the encoding of the token

app.config['SECRET_KEY'] = 'secretkey'

#SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database/foodtracking.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)



class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    eatenFood = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)


def token_requerido(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = NotImplemented

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'Message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'Message' : 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated

#Obtener todos los usuarios
@app.route('/user/all', methods = ['GET'])
@token_requerido
def obtener_usuarios(current_user):

    if not current_user.admin:
        return jsonify({'Message' : 'Cannot perform that function!'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'List of all users ' : output })

#Obtener user por ID
@app.route('/user/<public_id>', methods = ['GET'])
@token_requerido
def obtener_usuarioPorID(current_user,public_id):

    if not current_user.admin:
        return jsonify({'Message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Message' : 'No user has been found with public ID provided.'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    
    return jsonify({'User' : user_data}) 

#Crear usuario
@app.route('/user/add', methods = ['POST'])
@token_requerido
def crearUser(current_user):

    if not current_user.admin:
        return jsonify({'Message' : 'Cannot perform that function!'})

    data = request.get_json()
    #Hash de la password creada a partir del user and password
    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username= data['username'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Message' : 'The user has been created succesfully.'})


#Modificar/Promover usuario a Admin
@app.route('/user/<public_id>', methods = ['PUT'])
@token_requerido
def promoteUser(current_user,public_id):

    if not current_user.admin:
        return jsonify({'Message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Message ' : 'No user has been found.'})
    user.admin = True
    db.session.commit()
    
    return jsonify({'Message ' : 'The user has been promoted to admin. '})

#Eliminar usuario
@app.route('/user/<public_id>', methods = ['DELETE'])
@token_requerido
def removerUser(current_user,public_id):

    if not current_user.admin:
        return jsonify({'Message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'Message ' : 'No user has been found.'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'Message' : 'The user has been deleted'})


#Metodo de login, que permite generar un token para loguearse a partir de el user and password
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify ', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
            return make_response('Could not verify ', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    
    return make_response('Could not verify ', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/food/all', methods=['GET'])
@token_requerido
def obtener_Alimentos(current_user):

    foods = Food.query.filter_by(user_id= current_user.id).all()

    output = []

    for food in foods:
        food_data = {}
        food_data['id'] = food.id
        food_data['description'] = food.description
        food_data['eatenFood'] = food.eatenFood
        output.append(food_data)

    return jsonify({'Foods' : output})


@app.route('/food/<food_id>', methods=['GET'])
@token_requerido
def obtener_Alimento_porID(current_user,food_id): #current_id
    food = Food.query.filter_by(id=food_id, user_id=current_user.id).first()


    if not food:
        return jsonify({'Message': 'No food found.'})

    food_data = {}
    food_data['id'] = food.id
    food_data['description'] = food.description
    food_data['eatenFood'] = food.eatenFood

    return jsonify(food_data)  


@app.route('/food', methods=['POST'])
@token_requerido
def agregar_alimento(current_user):
    data =request.get_json()
    new_food = Food(description=data['description'], eatenFood=True, user_id= current_user.id)
    db.session.add(new_food)
    db.session.commit()
    return jsonify({'Message' : "Food added!"})


@app.route('/food/<food_id>', methods=['PUT'])
@token_requerido
def modificar_alimento(current_user,food_id):

    food = Food.query.filter_by(id=food_id, user_id=current_user.id).first()


    if not food:
        return jsonify({'Message': 'No food found.'})

    food.eatenFood = False
    db.session.commit()



    return jsonify({'Message' : 'The status of the food in your selected food eaten list has changed'})

@app.route('/food/<food_id>', methods=['DELETE'])
@token_requerido
def eliminar_alimento(current_user,food_id):
    food = Food.query.filter_by(id=food_id, user_id=current_user.id).first()

    if not food:
        return jsonify({'Message': 'No food found.'})

    db.session.delete(food)
    db.session.commit()

    return jsonify({'Message' : 'Food deleted.'})

