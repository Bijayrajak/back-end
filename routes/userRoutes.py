from flask_json import request, json_response,JsonError,jsonify
from flask import abort,json
from config import app,bcrypt,Session,api,login_manager,checkUser,hasExtraPayload
from sqlalchemy import exc,any_,or_
from sqlalchemy.exc import DataError,SQLAlchemyError
from flask_restplus import Resource,fields
from mymodals.swaggermodels import master_value,user_model,user_model_get,user_model_post,user_model_put,user_password_put
from routes import *
from flask_login import current_user,login_user,logout_user,login_required,fresh_login_required
from mymodals.mymodals import MetaDataMasterEntry,MetaUser,MetaAddress,MetaContacts,MetaUserImages
session = Session()
session.rollback()
name_space = api.namespace('user','Handling all user related data communication')

@name_space.route('/thistest',doc=False)
class MMainClass(Resource):    
    def get(self):
        print(type(current_user))
        if current_user.is_active:
            data='Logged in as : '+current_user.userName
        else: 
            data= 'not logged in'
        return {
        "status": "Got new data",
        "data": data
        }
    
    @fresh_login_required
    def post(self):
        if current_user.is_active:
            data='Logged in as : '+current_user.userName
        else: 
            data= 'not logged in'

        return {
        "status": "Posted new data",
        "data": data
        }
@name_space.route('/lookup/<string:key>')
class UserMasterEntry(Resource):

    @name_space.marshal_with(master_value, as_list=True)
    def get(self, key=None):
        if key:
            lookup_key = str(key).upper()
            try:
                masterEntries = session.query(MetaDataMasterEntry).filter(MetaDataMasterEntry.lookupKey==lookup_key).all()
            except:
                name_space.abort(404,message="No entries found")
                
            if masterEntries: 
                return [result.serialized for result in masterEntries]
            else:
                name_space.abort(404,message="No entries found")
        else:
            name_space.abort(400,message="Key parameter is missing, please verify")



@name_space.route('/<int:user_id>',methods=['GET'])
@name_space.route('/<int:last_record_offset>/<int:total_rows_next>',methods=['GET'])
@name_space.route('/',defaults={'user_id':None},methods=['GET'])
@name_space.route('/change/<int:user_id>',methods=['PUT'])
@name_space.route('/remove/<int:user_id>',methods=['DELETE'])
class NewUserClass(Resource):

    @login_required
    @name_space.marshal_with(user_model_get,as_list=True)
    def get(self,user_id=None,last_record_offset=None,total_rows_next=None):
        if not checkUser('ADMIN'):
            name_space.abort(403,message="Please contact your sytem adminstrator for this request")

        if (last_record_offset is not None) or (total_rows_next is not None):
            if total_rows_next>100 or total_rows_next<=0:
                name_space.abort(400, message='Row limit must be in range of 1 to 100')
        
        try:
            if user_id:
                userrsList = session.query(MetaUser).filter(MetaUser.userId==user_id).all()
            else:
                try:
                    userrsList=session.query(MetaUser).filter(MetaUser.userId>last_record_offset).limit(total_rows_next).all()
                except Exception:
                    session.rollback()
                    userrsList = session.query(MetaUser).all()
            if userrsList:
                return userrsList
            else:
                name_space.abort(400,message='No User Data found for the given ID input.')

        except Exception:
            session.rollback()
            name_space.abort(400,message="No such User Information Available,  Please verify.")

    @name_space.expect(user_model_put,validate=True)
    @login_required
    @name_space.marshal_with(user_model)
    def put(self,user_id):
        if not checkUser('ADMIN'):
            name_space.abort(403,message="Please contact your sytem adminstrator for this request")

        request_data=request.get_json(force=True)
        extra_payload =hasExtraPayload(request_data['newData'],user_model)
        if extra_payload:
            return name_space.abort(400,message='Unexpected key at payload :> '''+extra_payload)
        
        username_input_received=False
        email_input_received=False
        try:
            username_input=request_data['newData']['userName']
            username_input_received=True
            email_input=request_data['newData']['userEmail']
            email_input_received=True
        except KeyError:
            pass
        
        if username_input_received and not validUserName(username_input):
            return name_space.abort(400,message="Username must only have letters or numbers without spaces")
            
        if email_input_received and not isEmail(email_input):
            return name_space.abort(400,message="Not a Valid email format received.")

        try:
            userData=session.query(MetaUser).filter(MetaUser.userId==user_id)
            if userData.first():
                userData.update(request_data['newData'],synchronize_session=False)
                session.commit()
                return userData.first()
            else:
                name_space.abort(400,message='There is no such user data, Please verify.')

        except exc.IntegrityError as err:
            session.rollback()
            name_space.abort(403,message="This Username already exist, please try another username.")

        except DataError as ex:
            msg=str(ex.__dict__['orig'])
            if msg.find('URight')>0:
                message=request_data['newData']['_userRight']+ ' is unacceptable. Value must be either ["ADMIN","AUTHOR","PUBLISHER"]'
            elif msg.find('UStatus')>0:
                message=request_data['newData']['_userStatus']+' is unacceptable. Value must be either ["ACTIVE","INACTIVE","SUSPEND"] '
            else:
                message=ex.__dict__['orig']
            session.rollback()
            name_space.abort(400,message=message)

        except Exception as err:
            session.rollback()
            name_space.abort(400,message='There is no such user data, please check '+err.__str__())
    
    @login_required
    def delete(self,user_id):
        if not checkUser('ADMIN'):
            name_space.abort(403,message="Please contact your sytem adminstrator for this request")

        try:
            if (user_id==1):
                # return {'status':403,'message':'Change request received against the super User'}
                name_space.abort(403,message="Change request received against the super User",defect="Please Contact your system administrator.")
            elif (current_user.userId==user_id):
                name_space.abort(403,message="Please contact your system administrator to remove your information.")
            else:
                user_to_remove = session.query(MetaUser).filter(MetaUser.userId==user_id)
                if user_to_remove.first():
                    user_to_remove.deleted()
                else:
                    return {'message':"Request aborted , No such user Exist.", 'userId':user_id}
        except Exception as err:
            session.rollback()
            name_space.abort(400,message=err.__str__)


def isStrongPass(val):
    if not val:
        return False

    if len(val)<=7:
        return False
    else:
        if not hasUppercase(val):
           return False
        if not hasSpecialChar(val):
            return False
        if not hasLowercase(val):
            return False
        if not hasNumber(val):
            return False
            
    return True
            
def validUserName(val):
    if not val:
        return False

    if len(val)<=3:
        return False
    else:
        if not hasDotUnderscoreOnly(val):
            return False
        if re.search(' ',val):
            return False

    return True
        
def mapToAdminUser(user_id):
    pass


@name_space.route('/save',methods=['POST'])
@name_space.route('/changepass/<int:user_id>',methods=['PUT'])
@name_space.route('/list',methods=['GET'])
class UserClass(Resource):

    def get(self):
        try:
            userrsList = session.query(MetaUser).all()
            if userrsList:
                return [{'id':user.userId, 'username':user.userName } for user in userrsList]
            else:
                name_space.abort(400,message='No User Data found for the request')

        except Exception:
            session.rollback()
            name_space.abort(400,message="No User Information Available,  Please verify.")

    @name_space.expect(user_model_post,validate=True)
    @login_required
    @name_space.marshal_with(user_model_get,code=200)
    def post(self):
        if not checkUser('ADMIN'):
            name_space.abort(403,message="Please contact your sytem adminstrator for this request")

        data=request.get_json()
        try:
            password_input = data['password']
            username_input = data['userName']
            email_input=data['userEmail']

            if not isStrongPass(password_input):
                return name_space.abort(400,message="Not a Strong password, Include combination of uppercase numbers and specail characters as well(at least 6 characters).")

            if not validUserName(username_input):
                return name_space.abort(400,message="Username must only have letters or numbers without spaces")
            
            if not isEmail(email_input):
                return name_space.abort(400,message="Not a Valid email format received.")

            passwork = bcrypt.generate_password_hash(password_input).decode('utf-8')
            try:
                #preparing the address
                l1_address=data['address']['address_1']
                l2_address=data['address']['address_2'] if 'address_2' in data['address'].keys() else None
                l3_address=data['address']['address_3'] if 'address_3' in data['address'].keys() else None
                l4_address=data['address']['address_4'] if 'address_4' in data['address'].keys() else None
                #preparing the contact
                l1_contact=data['contactNo']['contact_1']
                l2_contact=data['contactNo']['contact_2'] if 'contact_2' in data['contactNo'].keys() else None
                l3_contact=data['contactNo']['contact_3'] if 'contact_3' in data['contactNo'].keys() else None
                l4_contact=data['contactNo']['contact_4'] if 'contact_4' in data['contactNo'].keys() else None
                address=MetaAddress(level1=l1_address,level2=l2_address,level3=l3_address,level4=l4_address)
                contact=MetaContacts(level1=l1_contact,level2=l2_contact,level3=l3_contact,level4=l4_contact)

                session.add_all([address,contact])
                session.commit()
            except KeyError as krr:
                name_space.abort(400,message="payload not defined properly for address and contact fields")
            except SQLAlchemyError as sqerr:
                name_space.abort(400,message=str(sqerr))

            user_type=data['userType']

            #option fields
            business_type = data['businessType'] if 'businessType' in data.keys() else ''
            organization_name = data['orgName'] if 'orgName' in data.keys() else ''
            first_name = data['firstName'] if 'firstName' in data.keys() else ''
            last_name = data['lastName'] if 'lastName' in data.keys() else ''
            user_gender = data['userGender'] if 'userGender' in data.keys() else ''
            user_dateofbirth = data['userDOB'] if 'userDOB' in data.keys() else None

            user = MetaUser(userType=user_type,
                            userName=username_input,
                            password=passwork,
                            userEmail=email_input,
                            address=address.addressId,
                            contactNo=contact.contactId,
                            businessType=business_type,
                            orgName=organization_name,
                            firstName=firstName,
                            lastName=last_name,
                            userGender=user_gender,
                            userDob=user_dateofbirth)
            # user = MetaUser(userName=username,password=passwork,userEmail=email,userstatus, schemaAccess=schema_access_ist,userRight=user_right)
            session.add(user)
            session.commit()
            return user
        except exc.IntegrityError:
            session.rollback()
            removeAddressAndContact(address.addressId,contact.contactId)
            name_space.abort(403,message="This User already exist, please try logging in")
            
        except DataError as ex:
            message=ex.__dict__['orig']
            session.rollback()
            removeAddressAndContact(address.addressId,contact.contactId)
            name_space.abort(400,message=message)
    
    @name_space.expect(user_password_put,validate=True)
    @login_required
    def put(self,user_id):
        if not checkUser('ADMIN'):
            name_space.abort(403,message="Please contact your sytem adminstrator for this request")

        request_data=request.get_json(force=True)
        try:
            password_input = request_data['new_password']['password']
            if not isStrongPass(password_input):
                return name_space.abort(400,message="Not a Strong password, Include combination of uppercase numbers and specail characters as well(at least 6 characters).")

            passwrok = bcrypt.generate_password_hash(password_input).decode('utf-8')
            user_to_update=session.query(MetaUser).filter(MetaUser.userId==user_id)
            if user_to_update.first():
                user_to_update.update({'password':passwrok},synchronize_session=False)
            else:
                return {'message':'Invalid User data detected','status':200}

            session.commit()
            return {'message':'Password Successfully changed','status':200}
        except Exception as err:
            session.rollback()
            name_space.abort(400,message='There is no such user data, please check '+err.__str__())

def removeAddressAndContact(address_id,contact_id):
    if address_id is None and contact_id is None:
        return "NO data to remove"
    else:
        try:
            session.query(MetaContacts).filter(MetaContacts.contactId==contact_id).delete(synchronize_session=False)
            session.query(MetaAddress).filter(MetaAddress.contactId==address_id).delete(synchronize_session=False)
            session.commit()
        except SQLAlchemyError as sqerr:
                name_space.abort(400,message=str(sqerr))
        
#model for the login params 
login_cred = api.model('loginModel',{'username':fields.String(required=True,description='username of the user'),'password':fields.String(required=True,description="password for the user"),'remember_me':fields.Boolean(required=True,description='Whether or not to remember the user if the browser is closed')})
@name_space.route('/login')
class LoginManager(Resource):
    
    @name_space.expect(login_cred,validate=True)
    def post(self):
        request_data = request.get_json(force=True)
        uname = request_data['username']
        upass = request_data['password']
        if len(uname)<1 or len(upass)<1:
            name_space.abort(400,message="Username and/or password shouldnot be empty.")

        rememberMe=request_data['remember_me']
        try:
            userdata= session.query(MetaUser).filter(MetaUser.userName==uname).first()
        except:
            session.rollback()
            name_space.abort(403,message="Unauthorized to login")
              
        try:
            if userdata and bcrypt.check_password_hash(userdata.password,upass):
                login_user(userdata,remember=rememberMe)
                return {
                    'message':"Success","user_id":userdata.userId,"username":uname,"status":userdata._userStatus,"role":userdata._userRight
                }
            else:
                return name_space.abort(400,message="Login Failed !!! Enter Valid Username and Password")
        except ValueError:
            session.rollback()
            return name_space.abort(403,message="Unauthorized to login")

    
'''
    This is the api block for user to be able to logout of the system and clear all of his session history

'''
@name_space.route('/logout')
class UserLogout(Resource):

    @login_required
    def post(self):
        logout_user()
        return {'status':200, 'message':'Logged out Successfully'}

'''
    This is the api designed to know about the user himself

'''
@name_space.route('/whoMI')
class KnowUser(Resource):

    @login_required
    @name_space.marshal_with(user_model)
    def get(self):
        if current_user.is_active:
            if current_user.is_authenticated:
                return current_user