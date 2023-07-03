
from flask import Blueprint, request,jsonify,Response
from flask_restful import Resource,Api
from user import *
from user.serializers import *
from JWTToken.JwtTokenGenerator import Tokengenerator

user_blueprint = Blueprint('userapi', __name__)
api = Api(user_blueprint)


class UserRegister(Resource):
    def post(self):
        if request.json['name'] and request.json['username'] and request.json['email'] and request.json['password'] and request.json['lastname']:
            if User.objects.filter(username=request.json['username']):
                return jsonify({"Error":"Username Already Exists..."})
            elif User.objects.filter(email=request.json['email']):
                return jsonify({"Error":"Email Already Exists..."})
            else:
                user=User(
                    name=request.json['name'],
                    username=request.json['username'],
                    email=request.json['email'],
                    lastname=request.json['lastname'],
                    is_superuser=request.json['is_superuser']
                    ).get_password(password=request.json['password'])
                user_schema = UserSchema()
                result = user_schema.dump(user)
                return  jsonify(result)
        else:
            return  jsonify({"Error":"Some Field Empty....."})
api.add_resource(UserRegister, '/create_user')


class Login(Resource):  
    def post(self):
            if request.json['username'] and request.json['password']:
                user=User.objects.filter(username=request.json['username']).first()
                if user and user.verify_password(request.json['password']):
                    (refresh_token,access_token)=Tokengenerator(str(user.id))
                    return jsonify({ 'refresh_token': refresh_token,'access_token': access_token})
                else:
                    return jsonify({'message': 'Invalid username or password'})
            else:
                return jsonify({'message': 'Some Field Empty...'})

    
api.add_resource(Login, '/login')

