from flask import Flask
from flask_restful import Api
from controllers import resources
from controllers import references
from controllers import Service
from controllers import jobs
from services import message, email
from controllers import users
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
api.add_resource(resources.ReferenceRegistration, '/api/v1/registration/user/<userId>/references', methods=['POST'])
api.add_resource(resources.AddServices, '/api/v1/registration/user/<userId>/services', methods=['POST'])
# Healt check
api.add_resource(resources.test, '/api/v1/test')
# Login
api.add_resource(resources.UserLogin, '/api/v1/login')
# Logout
api.add_resource(resources.UserLogoutAccess, '/api/v1/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/v1/logout/refresh')
# Token refresh
api.add_resource(resources.TokenRefresh, '/api/v1/token/refresh')
# Services
api.add_resource(Service.Services, '/api/v1/service', methods=['GET', 'POST'])
api.add_resource(Service.Service, '/api/v1/service/<serviceId>', methods=['GET'])
# Jobs
api.add_resource(jobs.Jobs, '/api/v1/jobs', methods=['GET', 'POST'])
api.add_resource(jobs.Job, '/api/v1/jobs/<jobId>', methods=['GET'])
# External email and message service
api.add_resource(message.sendMessage, '/api/v1/sendMessage/<number>', methods=['POST'])
api.add_resource(email.sendEmail, '/api/v1/sendEmail/<email>', methods=['POST'])
api.add_resource(references.ReferenceRegistration, '/api/v1/registration/references', methods=['POST'])
api.add_resource(references.SaveReferenceAnswers, '/api/v1/references/results', methods=['POST'])
# Add general questions
api.add_resource(generalQuestions.GeneralQuestions, '/api/v1/general-questions', methods=['POST', 'GET'])
# api.add_resource(generalQuestions.GeneralQuestions, '/api/general-question/<id>/update', methods=['PUT'])
# User
api.add_resource(users.users, '/api/v1/users', methods=['GET'])
api.add_resource(users.user, '/api/v1/users/<userId>', methods=['GET'])



#Registering database
DB_URI = "mongodb+srv://chameleon:kerberos@cluster0-sbsqw.mongodb.net/test?retryWrites=true&w=majority"
app.config['MONGODB_HOST'] = DB_URI
db = MongoEngine(app)