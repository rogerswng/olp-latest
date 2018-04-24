from flask import Flask, Response
from flask.ext.restful import Api, Resource
from flask_cors import CORS
from course import CreateCourse
from werkzeug.datastructures import Headers

# class MyResponse(Response):
#     # Override Default Response Class
#     def __init__(self, response=None, **kwargs):
#         kwargs['headers'] = ''
#         headers = kwargs.get('headers')
#         # 跨域控制
#         origin = ('Access-Control-Allow-Origin', '*')
#         methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
#         hs = ('Access-Control-Allow-Headers', 'content-type')
#         if headers:
#             headers.add(*origin)
#             headers.add(*methods)
#             headers.add(*hs)
#         else:
#             headers = Headers([origin, methods])
#         kwargs['headers'] = headers
#         return super().__init__(response, **kwargs)

application = app = Flask(__name__)
# app.response_class = MyResponse
api = Api(app)
CORS(app, origins='*', allow_headers='*')

api.add_resource(CreateCourse, '/createCourse', endpoint="createCourse")

if __name__ == '__main__':
    app.run(debug=True)
