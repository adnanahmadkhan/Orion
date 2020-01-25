from utilities import (
    min_length
)
from flask_restful import Resource, reqparse
from models import Jobs as jobs
import json

parser = reqparse.RequestParser()

class Jobs(Resource):
    def post(self):
        parser.add_argument('title', help='This field cannot be blank', required=True)
        parser.add_argument('job_description', help='This field cannot be blank', required=True)
        parser.add_argument('required_services', help='This field cannot be blank', action='append', required=True)
        parser.add_argument('start_date_to_apply', help='This field cannot be blank', required=True)
        parser.add_argument('last_date_to_apply', help='This field cannot be blank', required=True)
        parser.add_argument('pay', help='This field cannot be blank', required=True)
        print(parser)
        data = parser.parse_args()
        print(jobs)
        new_job = jobs.Jobs(
            title=data['title'],
            job_description=data['job_description'],
            required_services=data['required_services'],
            start_date_to_apply=data['start_date_to_apply'],
            last_date_to_apply=data['last_date_to_apply'],
            pay=data['pay']
        )

        try:
            print(new_job)
            new_job.save()
            return {
                'message': 'Job with title {} has been created'.format(data['title'])
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400

    def get(self):
        try:
            response = jobs.Jobs.objects.all()
            return {
                'response': '{}'.format(json.loads(response.to_json()))
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400

class Job(Resource):
    def get(self, jobId):
        try:
            response = jobs.Jobs.objects.get(id=jobId)
            print(response)
            return {
                'response': '{}'.format(json.loads(response.to_json()))
            }, 200
        except Exception as ex:
            print(ex)
            template = "{0}:{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return {'error': message}, 400
