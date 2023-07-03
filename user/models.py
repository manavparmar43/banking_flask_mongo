from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongo.database_conection import create_app
(app,db,ma)=create_app()


class User(db.Document):
    meta={'collection':'user'}
    name=db.StringField(required=True)
    lastname=db.StringField(required=True)
    username=db.StringField(required=True)
    email=db.StringField(required=True)
    password=db.StringField(required=True)
    is_superuser=db.BooleanField(default=False)

    def __repr__(self):
        return self.username
    
    def get_password(self,password):
        self.password = generate_password_hash(password)
        return super(User, self).save()
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)