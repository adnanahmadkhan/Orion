from utilities import (
    min_length
)
from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required
from models import Services as rt
import json
import pprint


parser = reqparse.RequestParser()

class Services(Resource):
    @jwt_required
    def post(self):
        parser.add_argument('service', help='This field cannot be blank', required=True)
        parser.add_argument('description')
        parser.add_argument('questions')
        print(parser)
        data = parser.parse_args()
        new_test = rt.Services(
            service=data['service'],
            description=data['description'],
            questions=data['questions']
        )

        try:
            print(new_test)
            new_test.save()
            return {
                'message': 'Service {} was created'.format(data['service'])
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400

    @jwt_required
    def get(self, id=None):
        result = {}
        try:
            response = rt.Services.objects.all()
            result['response'] = response
            return make_response(jsonify(result), 200)
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400

class Service(Resource):
    @jwt_required
    def get(self, serviceId):
        result = {}
        try:
            response = rt.Services.objects.get(id=serviceId)
            if not response:
                return {'error': 'Service doesn\'t exist'}, 404
            result['response'] = response
            return make_response(jsonify(result), 200)
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400
    
    @jwt_required
    def patch(self, serviceId):
        parser.add_argument('service')
        parser.add_argument('questions', action='append')
        parser.add_argument('description')
        data = parser.parse_args()
        insert = []

        if(not data["service"] or data["service"] is ""):
            del data["service"]
        if(not data["questions"] or data["questions"][0] is ""):
            del data["questions"]
        if(not data["description"] or data["description"] is ""):
            del data["description"]

        try:
            response = rt.Services.objects.get(id=serviceId)
            if not response:
                return {'error': 'Service doesn\'t exist'}, 404
            
            for item in list(data):
                if item is "service":
                    response.update(service=data[item])
                if item is "questions":
                    response.update(questions=data[item] + response.questions)
                if item is "description":
                    response.update(description=data[item])

            
            return {
                'response': 'Service has been updated'
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400
    
    @jwt_required
    def delete(self, serviceId):
        try:
            response = rt.Services.objects.get(id=serviceId)
            if not response:
                return {'error': 'Job doesn\'t exist'}, 404
            updated_service = response.delete()
            print(updated_service)
            return {
                'response': 'Service has been deleted'
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400