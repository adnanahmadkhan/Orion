from flask import Flask
from flask_restful import Api
from controllers import resources
from controllers import Service as rt
from services import message, email
from controllers import generalQuestions
from models.RevokedTokens import RevokedTokens
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

# JWT
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokens.is_jti_blacklisted(jti)



# Registering endpoints
api.add_resource(resources.InitialRegistration, '/api/v1/registration/initial')
api.add_resource(resources.AddPersonalDetails, '/api/v1/registration/personal-details/<userId>')
api.add_resource(resources.AddEmergencyContact, '/api/v1/registration/user/<userId>/emergency-contact-details', methods=['POST'])
api.add_resource(resources.AddEmployementHistory, '/api/v1/registration/user/<userId>/employement-details', methods=['POST'])
api.add_resource(resources.AddGeneralQuestionAnswer, '/api/v1/registration/user/<userId>/general-question-answers', methods=['POST'])
api.add_resource(resources.UpdateUserType, '/api/v1/registration/user/<userId>/update-user-type', methods=['PATCH'])
api.add_resource(resources.test, '/api/v1/test')
api.add_resource(resources.UserLogin, '/api/v1/login')
api.add_resource(resources.UserLogoutAccess, '/api/v1/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/v1/logout/refresh')
api.add_resource(resources.TokenRefresh, '/api/v1/token/refresh')
# api.add_resource(rt.RecruitmentTest, '/api/v1/recruitmentTest/<id>', methods=['GET', 'PATCH', 'DELETE'], )
api.add_resource(rt.Service, '/api/v1/service', methods=['GET', 'POST'])
api.add_resource(message.sendMessage, '/api/v1/sendMessage/<number>', methods=['POST'])
api.add_resource(email.sendEmail, '/api/v1/sendEmail/<email>', methods=['POST'])
api.add_resource(resources.ReferenceRegistration, '/api/v1/registration/user/<userId>/references', methods=['POST'])
api.add_resource(resources.AddServices, '/api/v1/registration/user/<userId>/services', methods=['POST'])
api.add_resource(generalQuestions.GeneralQuestions, '/api/v1/general-questions', methods=['POST', 'GET'])
# api.add_resource(generalQuestions.GeneralQuestions, '/api/general-question/<id>/update', methods=['PUT'])


#Registering database
DB_URI = "mongodb+srv://chameleon:kerberos@cluster0-sbsqw.mongodb.net/test?retryWrites=true&w=majority"
app.config['MONGODB_HOST'] = DB_URI
db = MongoEngine(app)