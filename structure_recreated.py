from config import Base
from config import engine,Session,bcrypt
from mymodals.mymodals import MetaUser,MetaDataMasterEntry,MetaUserTypeLookup,MetaOrganizationTypeLookup,MetaImageTypeLookup,MetaContacts,MetaAddress

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session=Session()
if not session.query(MetaAddress).first():
    address = MetaAddress('kathmandu')
    session.add(address)
    session.commit()

if not session.query(MetaContacts).first():
    contact = MetaContacts(level1=9235400844)
    session.add(contact)
    session.commit()

if not session.query(MetaUserTypeLookup).first():
    component_type1='USER'

    user_entry1=MetaUserTypeLookup(typeIndex=component_type1,typeDescription='CLIENT',typeRemarks='type of the user for the portal')
    user_entry2=MetaUserTypeLookup(typeIndex=component_type1,typeDescription='PUBLICUSER',typeRemarks='type of the user for the portal')

    masterEntries= [user_entry1,user_entry2]
    session.add_all(masterEntries)
    session.commit()

if not session.query(MetaOrganizationTypeLookup).first():
    component_type2='ORGANIZATION'

    org_entry1=MetaOrganizationTypeLookup(typeIndex=component_type2,typeDescription="ORG1",typeRemarks='type of the organizations associated with the portal')
    org_entry2=MetaOrganizationTypeLookup(typeIndex=component_type2,typeDescription="ORG2",typeRemarks='type of the organizations associated with the portal')

    masterEntries= [org_entry1,org_entry2]
    session.add_all(masterEntries)
    session.commit()

if not session.query(MetaImageTypeLookup).first():
    component_type3='USERIMAGEFOR'
    
    imagetype_entry1=MetaImageTypeLookup(typeIndex=component_type3,typeDescription="BANNER",typeRemarks='what type of image is this.')
    imagetype_entry2=MetaImageTypeLookup(typeIndex=component_type3,typeDescription="LOGO",typeRemarks='what type of image is this.')
    imagetype_entry3=MetaImageTypeLookup(typeIndex=component_type3,typeDescription="PROFILE",typeRemarks='what type of image is this.')

    masterEntries= [imagetype_entry1,imagetype_entry2,imagetype_entry3]
    session.add_all(masterEntries)
    session.commit()

if not session.query(MetaUser).first():
    user = MetaUser(userName='Admin01',
                    userType=1,
                    password=bcrypt.generate_password_hash('Nepal@1234').decode('utf-8'),
                    userEmail='admin@admin.com',
                    address=1,
                    contactNo=1
                    )
    session.add(user)
    session.commit()
