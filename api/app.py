from flask import Flask, Response
from flask.ext.restful import Api, Resource
from flask_cors import CORS
from course import CreateCourse, TeacherCourseList

application = app = Flask(__name__)
# app.response_class = MyResponse
api = Api(app)
CORS(app, origins='*', allow_headers='*')

api.add_resource(CreateCourse, '/createCourse', endpoint="createCourse")
api.add_resource(TeacherCourseList, '/teacherCourseList')

if __name__ == '__main__':
    app.run(debug=True)
