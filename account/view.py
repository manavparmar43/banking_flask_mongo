from flask import Blueprint,jsonify,request
from flask_restful import Resource,Api
from account.serializers import *
from account.models import *
from user.models import *
from flask_jwt_extended import  jwt_required, get_jwt_identity
import random

account_bp=Blueprint("accountapi",__name__)
api=Api(account_bp)


class IdentifyDetailsApi(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            identify_details=IdentifyDetails(
                user=user.id,
                pancard=request.json['pancard'],
                adharcard=request.json['adharcard'],
                phone=request.json['phone'],
                ).save()
            identify_details_schema=IdentifyDetailsSchema()
            identify_details_data=identify_details_schema.dump(identify_details)
            return jsonify({"Identify-Details":identify_details_data})
        else:
            return jsonify({"Error":"only admin can add data"})
        
    

api.add_resource(IdentifyDetailsApi,"/identifydetails-create")

class IdentifyDetailsUpdateDeleteApi(Resource):
    @jwt_required()
    def put(self,id):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if id:
                identify_details=IdentifyDetails.objects.filter(id=id).first()
                identify_details.pancard=request.json['pancard']
                identify_details.adharcard=request.json['adharcard']
                identify_details.phone=request.json['phone']
                identify_details.save()
                identify_details_schema=IdentifyDetailsSchema()
                identify_details_data=identify_details_schema.dump(identify_details)
                return jsonify({"Identify-Details":identify_details_data})
            else:
                return jsonify({"Error":"Not Found"})
        else:
            return jsonify({"Error":"only admin can Update data"})
    
    def delete(self,id):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if id:
                identify_details=IdentifyDetails.objects.filter(id=id).first()
                identify_details.delete()
                return jsonify({"Delete-Succcess":"Delete Successfully...."})
            else:
                return jsonify({"Error":"Not Found"})
        else:
            return jsonify({"Error":"only admin can Delete data"})
        
api.add_resource(IdentifyDetailsUpdateDeleteApi,"/identifydetails-update-delete/<string:id>") 

class AccountApi(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if IdentifyDetails.objects.filter(identify=request.json['identify']):
                account=Account(
                    user=user.id,
                    bank=request.json['bank'],
                    account_number=random.getrandbits(50),
                    customer_name=user.name,
                    identify=request.json['identify'],
                    city=request.json['city'],
                    account_created=request.json['account_created'],
                    ).save()
                account_schema=AccountSchema()
                account_data=account_schema.dump(account)
                return jsonify({"Account-Data":account_data})
            else:
               return jsonify({"Error":"Identify Detail not found"}) 
        else:
            return jsonify({"Error":"only admin can add data"})

api.add_resource(AccountApi,"/account-create")


class ActiveAccount(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser: 
            account=Account.objects.filter(activate=False)
            account_schema=AccountSchema()
            account_data=account_schema.dump(account)
            return jsonify({"Data":account_data})
        else:
            return jsonify({"Error":"Only admin can see the account active detail"})
        
    def post(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            account=Account.objects.filter(id=request.json['id']).first()
            if account:
                    account.activate=True
                    account.save()
                    account_schema=AccountSchema()
                    account_data=account_schema.dump(account)
                    return jsonify({"Activate-Successfully":account_data})
            else:
                return jsonify({"Error":"Account Not Finding..."})
        else:
            return jsonify({"Error":"Only admin can  active the account"})


api.add_resource(ActiveAccount,"/active-account")

class BalanceApi(Resource):
    @jwt_required()
    def get():
        current_user = get_jwt_identity()
        if User.objects.filter(id=current_user):
           identify=IdentifyDetails.objects.filter(user__id=current_user).first()
           if identify:
                account=Account.objects.filter(identify__id=identify.id).first()
                if account.activate:
                    balance=Balance.objects.filter(account__id=account.id).first()
                    balance_schema=BalanceSchema()
                    balance_data=balance_schema.dump(balance)
                    return jsonify({"Data":balance_data})
                else:
                    return jsonify({"Error":"Account not activate"})
           else:
               return jsonify({"Error":"identify not found"})


    def post(self):
        current_user = get_jwt_identity()
        if User.objects.filter(id=current_user):
            account=Account.objects.filter(id=request.json['account']).first()
            if account:
               if account.activate:
                Balance(account=request.json['account'],balance=request.json['balance']).save()
                return jsonify({"Success":"Balance Added..."})
               else:
                  return jsonify({"Error":"Account not activate..."}) 
            else:
               return jsonify({"Error":"Account not found..."})  
        else:
            return jsonify({"Error":"User Not Found..."})
api.add_resource(BalanceApi,"/balance")


class Transaction(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if User.objects.filter(id=current_user): 
            identify=IdentifyDetails.objects.filter(user__id=current_user).first()
            if identify:
                account=Account.objects.filter(identify__id=identify.id).first()
                if account.activate:
                    balance=Balance.objects.filter(account__id=account.id).first()
                    if int(balance.balance) >0:
                        if int(balance.balance) >= int(request.json['transaction_money']):
                            transaction=Transaction(balance=balance.id,
                                        transaction_money=request.json['transaction_money'],
                                        received_account_number=request.json['received_account_number'],
                                        received_bank_name=request.json['received_bank_name'],
                                        received_bank_ifscode=request.json['received_bank_ifscode']).save()
                            transaction_schema=TransactionSchema()
                            transaction_data=transaction_schema.dump(transaction)
                            balance.balance=int(balance.balance) - int(request.json['transaction_money'])
                            balance.save()
                            return jsonify({"Successfully":transaction_data})
                        else:
                            return jsonify({"Error":"Insufficient Balance...."})
                    else:
                        return jsonify({"Error":"Insufficient Balance...."})
                else:
                    return jsonify({"Error":"Account Deactivate...."})
            else:
                return jsonify({"Error":"Identify not found...."})
        else:
            return jsonify({"Error":"User not found...."})
