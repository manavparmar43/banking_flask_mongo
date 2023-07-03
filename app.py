from flask import current_app
from mongo.database_conection import *
from flask_jwt_extended import JWTManager
import datetime

(app,db,ma)=create_app()

app.config['JWT_SECRET_KEY']="3d6f45a5fc12445dbac2f59c3b6c7cb1"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=120)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
# export FLASK_ENV=development
jwt = JWTManager(app)
from user.view import user_blueprint
from JWTToken.JwtTokenGenerator import token_blueprint
from Bank.view import bank_bp
from account.view import account_bp
# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(token_blueprint)
app.register_blueprint(bank_bp)
app.register_blueprint(account_bp)
if __name__ == '__main__':
    app.run()