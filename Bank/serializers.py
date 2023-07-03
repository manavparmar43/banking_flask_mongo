
from mongo.database_conection import *
from Bank.models import *

(app,db,ma)=create_app()


class BankSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = Bank
        fields=('id',"bank_name","branch_name","ifsc_code","country","city","area_code")







    
