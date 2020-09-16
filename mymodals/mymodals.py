from sqlalchemy import Column, Integer,String,Enum,ARRAY,DateTime,UniqueConstraint,ForeignKeyConstraint,BOOLEAN,CheckConstraint,Text,BLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from config import Base,engine,Session,login_manager
from flask_login import UserMixin


#creating the userloader block to fetch the currenlty logged in user
session = Session()
@login_manager.user_loader
def load_user(userId):
    return session.query(MetaUser).filter(MetaUser.userId==userId).first()

class MetaDataMasterEntry(Base):
    __tablename__='master_lookup'
    lookupId = Column(Integer,primary_key=True)
    lookupKey = Column(String(25), nullable=False)
    lookupValue=Column(Text,nullable=False, unique=True)
    remarks=Column(Text,nullable=True)

    def __init__(self,lookupKey,lookupValue,remarks=None):
        self.lookupKey=lookupKey
        self.lookupValue=lookupValue
        self.remarks=remarks
    
    @property
    def serialized(self):
        return {
            'lookup_id':self.lookupId,
            'lookup_key':self.lookupKey,
            'lookup_value':self.lookupValue,
            'remarks':self.remarks
        }
        

class MetaAddress(Base):
    __tablename__='portal_address_details'
    addressId=Column(Integer,primary_key=True)
    level1=Column(String(200),nullable=False)
    level2=Column(String(200))
    level3=Column(String(200))
    level4=Column(String(200))

    def __init__(self,level1,level2=None,level3=None,level4=None):
        self.level1=level1
        self.level2=level2
        self.level3=level3
        self.level4=level4
    
    @property
    def serialized(self):
        return {
            'address_id':self.addressId,
            'address_1':self.level1,
            'address_2':self.level4,
            'address_3':self.level3,
            'address_4':self.level4
        }

class MetaContacts(Base):
    __tablename__='portal_contact_details'
    contactId=Column(Integer,primary_key=True)
    contact1=Column(String(200),nullable=False)
    contact2=Column(String(200))
    contact3=Column(String(200))
    contact4=Column(String(200))

    def __init__(self,level1,level2=None,level3=None,level4=None):
        self.contact1=level1
        self.contact2=level2
        self.contact3=level3
        self.contact4=level4
    
    @property
    def serialized(self):
        return {
            'contact_id':self.contactId,
            'contact_1':self.contact1,
            'contact_2':self.contact2,
            'contact_3':self.contact3,
            'contact_4':self.contact4
        }


class MetaUserTypeLookup(Base):
    #component can be user,business,imageType,etc
    __tablename__='portal_UserType_lookup'
    typeId=Column(Integer,primary_key=True)
    typeIndex=Column(String(100),nullable=False)
    typeDescription=Column(String(200),nullable=False)
    typeRemarks=Column(String(200))
    UniqueConstraint(typeDescription,typeIndex,name='unq_usertype_desc_for_index')

    def __init__(self,typeIndex,typeDescription,typeRemarks=None):
        self.typeIndex=typeIndex
        self.typeDescription=typeDescription
        self.typeRemarks=typeRemarks

    @property
    def serialized(self):
        return {
            'type_id':self.typeId,
            'type_name':self.typeIndex,
            'type_description':self.typeDescription,
            'type_remarks':self.typeRemarks
        }
class MetaOrganizationTypeLookup(Base):
    #component can be user,business,imageType,etc
    __tablename__='portal_OrganizaitonType_lookup'
    typeId=Column(Integer,primary_key=True)
    typeIndex=Column(String(100),nullable=False)
    typeDescription=Column(String(200),nullable=False)
    typeRemarks=Column(String(200))
    UniqueConstraint(typeDescription,typeIndex,name='unq_orgtype_desc_for_index')

    def __init__(self,typeIndex,typeDescription,typeRemarks=None):
        self.typeIndex=typeIndex
        self.typeDescription=typeDescription
        self.typeRemarks=typeRemarks

    @property
    def serialized(self):
        return {
            'type_id':self.typeId,
            'type_name':self.typeIndex,
            'type_description':self.typeDescription,
            'type_remarks':self.typeRemarks
        }

class MetaImageTypeLookup(Base):
    #component can be user,business,imageType,etc
    __tablename__='portal_ImageType_lookup'
    typeId=Column(Integer,primary_key=True)
    typeIndex=Column(String(100),nullable=False)
    typeDescription=Column(String(200),nullable=False)
    typeRemarks=Column(String(200))
    UniqueConstraint(typeDescription,typeIndex,name='unq_imagetype_desc_for_index')

    def __init__(self,typeIndex,typeDescription,typeRemarks=None):
        self.typeIndex=typeIndex
        self.typeDescription=typeDescription
        self.typeRemarks=typeRemarks

    @property
    def serialized(self):
        return {
            'type_id':self.typeId,
            'type_name':self.typeIndex,
            'type_description':self.typeDescription,
            'type_remarks':self.typeRemarks
        }

class MetaUser(Base,UserMixin):
    __tablename__='portal_users'
    userId = Column(Integer,primary_key=True)
    userType=Column(Integer,nullable=False)
    userName = Column(String(20),nullable=False)
    password = Column(String(60),nullable=False)
    userEmail = Column(String(40),nullable=False)
    address=Column(Integer,nullable=False)
    contactNo=Column(Integer,nullable=False)
    businessType=Column(Integer)
    orgName=Column(String(500))
    firstName = Column(String(50))
    lastName = Column(String(50))
    userGender=Column(String,Enum('MALE','FEMALE','OTHERS',name='UserGender'))
    userDOB=Column(DateTime)
    createdOn=Column(DateTime,default=datetime.now)
    updatedOn=Column(DateTime)
    UniqueConstraint(userName, name='same_user_entry')  
    ForeignKeyConstraint([userType],[MetaUserTypeLookup.typeId],name='fk_user_types')
    ForeignKeyConstraint([businessType],[MetaOrganizationTypeLookup.typeId],name='fk_user_business_types')
    ForeignKeyConstraint([address],[MetaAddress.addressId],name='fk_user_address')
    ForeignKeyConstraint([contactNo],[MetaContacts.contactId],name='fk_user_contacts')

    def __init__(self,userType,userName,password,userEmail,address,contactNo,businessType=None,orgName=None,firstName=None,lastName=None,userGender=None,userDob=None):
        self.userType=userType
        self.userName=userName
        self.password=password
        self.userEmail=userEmail
        self.address=address
        self.contactNo=contactNo
        self.businessType=businessType
        self.orgName=orgName
        self.firstName=firstName
        self.lastName=lastName
        self.userGender=userGender
        self.userDOB=userDob

    def get_id(self):
        return self.userId

    @property
    def serialized(self):
        return { 'userId':self.userId,
                 'user_name':self.userName,
                 'password':self.password,
                 'user_email':self.userEmail,
                 'address':self.address,
                 'user_type':self.userType,
                 'contact_number':self.contactNo,
                 'business_type':self.businessType,
                 'organization_name':self.orgName,
                 'first_name':self.firstName,
                 'last_name':self.lastName,
                 'user_gender':self.userGender,
                 'user_date_of_birth':self.userDOB,
                 'updated_on':self.updatedOn,
                 'created_on':self.createdOn
                }
    
    def __repr__(self):
        return f'{{userId={self.userId},userName={self.userName},password={self.password},userEmail={self.userEmail},createdOn={self.createdOn} }}'

class MetaUserImages(Base):
    #component can be user,business,etc
    __tablename__='portal_images'
    imageId=Column(Integer,primary_key=True)
    imageName=Column(String(100),nullable=False)
    imageData=Column(Text,nullable=False)
    imageFor=Column(Integer,nullable=False)
    userId=Column(Integer,nullable=False)
    ForeignKeyConstraint([userId],[MetaUser.userId],name='fk_image_users') 
    ForeignKeyConstraint([imageFor],[MetaImageTypeLookup.typeId],name='fk_image_componenttype')

    def __init__(self,imageName,imageData,imageFor,userId):
        self.imageName=imageName
        self.imageData=imageData
        self.imageFor=imageFor
        self.userId=userId

    @property
    def serialized(self):
        return {
            'image_id':self.imageId,
            'image_name':self.imageName,
            'image_for':self.imageFor,
            'user_id':self.userId
        }


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)