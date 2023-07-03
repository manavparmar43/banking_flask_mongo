from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_restful import Resource,Api
from flask import jsonify,Blueprint
token_blueprint = Blueprint('tokenapi', __name__)
api = Api(token_blueprint)
def Tokengenerator(id):
    refresh_token = create_refresh_token(identity=id)
    access_token = create_access_token(identity=id)

    return refresh_token,access_token


class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()

        access_token = create_access_token(identity=current_user_id)

        return jsonify({'access_token': access_token})
    

api.add_resource(Refresh, '/refresh')