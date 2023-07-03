
from mongo.database_conection import *
from user.models import *

(app,db,ma)=create_app()


class UserSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = User
        fields=('id','name',"lastname",'username','email','password','is_superuser')







    
