
from mongo.database_conection import *
from account.models import *

(app,db,ma)=create_app()


class AccountSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = Account
        fields=('id',"user","bank","account_number","customer_name","city","account_created","activate")

class IdentifyDetailsSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = IdentifyDetails
        fields=('id',"user","pancard","adharcard","phone")

class BalanceSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = Balance
        fields=('id',"account","balance")

class TransactionSchema(ma.Schema):
    id=ma.String()
    class Meta:
        model = Transaction
        fields=('id',"balance","transaction_money","transaction_date","received_account_number","received_bank_name","received_bank_ifscode")