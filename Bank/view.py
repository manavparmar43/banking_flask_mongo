from flask import Blueprint,jsonify,request
from flask_restful import Resource,Api
from Bank.serializers import *
from Bank.models import *
from user.models import *
from flask_jwt_extended import  jwt_required, get_jwt_identity
bank_bp=Blueprint("bankapi",__name__)
api=Api(bank_bp)

class BankAddApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            bank=Bank.objects.all()
            bank_schema=BankSchema()
            bank_data=bank_schema.dump(bank)
            return jsonify({"Bank-data":bank_data})
        else:
            return jsonify({"Error":"only admin can access...."})
    def post(self):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if request.json['bank_name'] and request.json['branch_name'] and request.json['ifsc_code'] and request.json['country'] and request.json['city'] and request.json['area_code']:
                if Bank.objects.filter(ifsc_code=request.json['ifsc_code']):
                    return jsonify({"Error":"IFSC Code already added.."})
                else:
                    bank=Bank(

                            bank_name=request.json['bank_name'],
                            branch_name=request.json['branch_name'],
                            ifsc_code=request.json['ifsc_code'],
                            country=request.json['country'],
                            city=request.json['city'],
                            area_code=request.json['area_code']
                            
                    )
                    bank.save()
                    bank_schema=BankSchema()
                    bank_data=bank_schema.dump(bank)
                    return jsonify({"Bank-Data":bank_data})
            else:
                return jsonify({"Error":"Some Field Empty...."})
        else:
            return jsonify({"Error":"only admin can access...."})
        
api.add_resource(BankAddApi,'/add-bank')



class BankUpdateDeleteApi(Resource):
    @jwt_required()
    def put(self,id):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if id:
                bank=Bank.objects.filter(id=str(id)).first()
                if bank:
                    if request.json:
                        bank.bank_name=request.json['bank_name']
                        bank.branch_name=request.json['branch_name']
                        bank.ifsc_code =  request.json['ifsc_code']
                        bank.country=request.json['country']
                        bank.city=request.json['city']
                        bank.area_code=request.json['area_code']
                        bank.save()
                        bank_schema=BankSchema()
                        bank_data=bank_schema.dump(bank)
                        return jsonify({"Data":bank_data})
                    else:
                        return jsonify({"Error":"No any Update"})
                else:
                    return jsonify({"Error":"No any Bank Found"})
        else:
            return jsonify({"Error":"only admin can access...."})
    def delete(self,id):
        current_user = get_jwt_identity()
        user=User.objects.filter(id=current_user).first()
        if user.is_superuser:
            if id:
                if Bank.objects.filter(id=str(id)):
                    Bank.objects.filter(id=str(id)).first().delete()
                    return jsonify({"Success":"Bank Record Deleted Successfully"})
                else:
                    return jsonify({"Error":"No any Bank Found"})
            else:
                return jsonify({"Error":"Id not found"})
        else:
            return jsonify({"Error":"only admin can access...."})


api.add_resource(BankUpdateDeleteApi,'/update-bank/<string:id>')