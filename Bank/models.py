# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_mongoengine import Document
from mongo.database_conection import create_app
(app,db,ma)=create_app()

class Bank(db.Document):
    meta={'collection':'bank'}
    bank_name=db.StringField(required=True)
    branch_name=db.StringField(required=True)
    ifsc_code=db.StringField(required=True)
    country=db.StringField(required=True)
    city=db.StringField(required=True)
    area_code=db.StringField(required=True)

    def __repr__(self):
        return self.bank_name

