# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_mongoengine import Document
from datetime import date
from Bank.models import Bank
from user.models import User
import datetime
from mongo.database_conection import create_app
(app,db,ma)=create_app()

class IdentifyDetails(db.Document):
    meta={'collection':'IdentifyDetails'}
    user=db.ReferenceField(User, nullabel=True)
    pancard=db.StringField(required=True)
    adharcard=db.StringField(required=True)
    phone=db.StringField(required=True)
    
    def __repr__(self):
        return self.pancard

class Account(db.Document):
    meta={'collection':'account'}
    bank=db.ReferenceField(Bank, nullabel=True)
    identify=db.ReferenceField(IdentifyDetails, nullabel=True)
    account_number=db.StringField(required=True)
    customer_name=db.StringField(required=True)
    city=db.StringField(required=True)
    account_created=db.DateField(default= date.today())
    activate= db.BooleanField(default=False)

    def __repr__(self):
        return self.customer_name
    
class Balance(db.Document):
   meta={'collection':'BalanceMoney'}
   account=db.ReferenceField(Account, nullabel=True)
   balance=db.StringField(required=True)
   
   def __repr__(self):
        return self.account
   

class Transaction(db.Document):
    meta={"collection":"Transaction"}
    balance=db.ReferenceField(Balance, nullabel=True)
    transaction_money=db.StringField(required=True)
    transaction_date=db.DateTimeField(default=datetime.datetime.utcnow) 
    received_account_number=db.StringField(required=True)
    received_bank_name=db.StringField(required=True)
    received_bank_ifscode=db.StringField(required=True)

    def __repr__(self):
        return self.account
   