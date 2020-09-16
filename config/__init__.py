from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from flask_restplus import Api,fields
import configparser,os
from datetime import timedelta
#flask_login for user session management
from flask_login import LoginManager,current_user
from flask_cors import CORS

#list of predefined values

#preparing the configuration information for initializing th system
config_data = configparser.RawConfigParser()
print(os.path.join(os.path.dirname(__file__), 'application.properties'))

config_categrory='DEVDATABASECRED'
config_data.readfp(open(os.path.abspath('./application.properties')))
dailect_name=config_data.get(config_categrory,'dailect')
username=config_data.get(config_categrory,'username')
password=config_data.get(config_categrory,'password')
db_ip = config_data.get(config_categrory,'database.ip')
db_port = config_data.get(config_categrory,'database.port')
dbname=config_data.get(config_categrory,'database.name')
schema_name=config_data.get(config_categrory,'database.schema')
secretkey = config_data.get('APPCONFIGURATIONS','secretKey')
sessionTimeout=config_data.getint('APPCONFIGURATIONS','session_timeout_minutes')
    
#initializing the flask application
app = Flask(__name__)

app.config['SECRET_KEY']=secretkey
app.config['RESTPLUS_VALIDATE']=True
engine = create_engine(dailect_name+'://'+username+':'+password+'@'+db_ip+':'+db_port+'/'+dbname,echo=True)
Base = declarative_base()
Base.metadata= MetaData(schema=schema_name)
bcrypt = Bcrypt(app)
fjson = FlaskJSON(app)
Session = sessionmaker()
Session.configure(bind=engine)
#enabling the cors support for the backend
CORS(app)
#setting up the restplus config for the swagger implemetation
api = Api(app)

login_manager = LoginManager(app=app)
app.config['REMEMBER_COOKIE_DURATION']=timedelta(minutes=sessionTimeout)


@login_manager.unauthorized_handler
def unauthorized():
    return { 'status':403, 'message':'Please Login first to user metadata manager services.', 'loginat':'/user/login'}

def checkUser(right):
    if not current_user.is_anonymous:
        return current_user._userRight==right
    else:
        return False

def hasExtraPayload(request_payload,*api_model):
    for keyval in request_payload.keys():
        found=False
        for model in api_model:
            if keyval in model.keys():
                found=True
                break
        if not found:
            return keyval
    return False

from routes import userRoutes