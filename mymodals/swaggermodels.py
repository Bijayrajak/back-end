from config import api,app
from flask_restplus import fields
from werkzeug.datastructures import FileStorage


# defining the model for Lookup master vallue response
master_value = api.model('master_lookup_val',{'lookup_value':fields.String,'remarks':fields.String})

# defining the model for address vallue response
addressModel = api.model('address_model_val',{  'address_1':fields.String(required=True),
                                                'address_2':fields.String,
                                                'address_3':fields.String,
                                                'address_4':fields.String
                                                })
addressModel_get=api.inherit('address_model_val_get',addressModel,{'address_id':fields.Integer})


# defining the model for contact vallue response
contactModel = api.model('contact_val',{        'contact_1':fields.String(required=True),
                                                'contact_2':fields.String,
                                                'contact_3':fields.String,
                                                'contact_4':fields.String})

contactModel_get=api.inherit('contact_model_val_get',contactModel,{'contact_id':fields.Integer})

# defining the model for userobject response and request
user_model=api.model('user_general_info',{'user_name':fields.String,
                                           'user_email':fields.String,
                                           'address':fields.Nested(addressModel_get),
                                           'user_type':fields.Integer,
                                           'contact_number':fields.Nested(contactModel_get),
                                           'business_type':fields.Integer,
                                           'organization_name':fields.String,
                                            'first_name':fields.String,
                                            'last_name':fields.String,
                                            'user_gender':fields.String,
                                            'user_date_of_birth':fields.Date,
                                            'updated_on':fields.DateTime,
                                           'createdOn':fields.DateTime})


user_model_get=api.inherit('user_get_info',user_model,{'user_id':fields.Integer})

user_model_post = api.model('user_data_post',{      'userType':fields.Integer,
                                                    'userName' :fields.String,
                                                    'password' : fields.String,
                                                    'userEmail' :fields.String,
                                                    'address':fields.Nested(addressModel),
                                                    'contactNo':fields.Nested(contactModel),
                                                    'businessType':fields.String,
                                                    'orgName':fields.String,
                                                    'firstName' : fields.String,
                                                    'lastName' : fields.String,
                                                    'userGender':fields.String(enum=['MALE','FEMALE','OTHERS'],default="MALE"),
                                                    'userDOB':fields.DateTime,
                                                })

user_model_put = api.model('user_data_put',{"newData":fields.Nested(user_model_post,required=True)})

user_password_put = api.model('user_pass_put',{"new_password":fields.Nested(api.model('password_param',{'password':fields.String(required=True) }),required=True)})
