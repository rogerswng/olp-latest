from flask import Flask, Response
from flask.ext.restful import Api, Resource
from flask_cors import CORS
# from dbop import Mysql

# Database Connector Pool Initialize
# db = Mysql()

application = app = Flask(__name__)
# app.response_class = MyResponse
api = Api(app)
CORS(app, origins='*', allow_headers='*')

from course import CreateCourse, TeacherCourseList, StudentCourseList
from course import CourseDetail, CourseTitle, CreateTopic, TopicTitle, EditTopic
from course import VideoUpload, PicUpload
from course import CreateSection, SectionDetail, SectionList, UpdateSectionProcess
from course import StudentProcessCourse
from course import StudentNameList, ImportStudent
from course import EditCourse, CreateMdFile, EditSection
from practice import CreatePractice, EditPractice
from practice import StudentPracticeList, PracticeBasic, FetchProblems, MarkPractice, SavePracticeDraft
from practice import TeacherPracticeList
from practice import CreateProblem, EditProblem
from login import Login
from testreverseproxy import TestReverseProxy

api.add_resource(TestReverseProxy, '/testReverseProxy')

api.add_resource(CreatePractice, '/createPractice')
api.add_resource(EditPractice, '/editPractice')
api.add_resource(CreateProblem, '/createProblem')
api.add_resource(EditProblem, '/editProblem')
api.add_resource(StudentPracticeList, '/studentPracticeList')
api.add_resource(TeacherPracticeList, '/teacherPracticeList')
api.add_resource(PracticeBasic, '/practiceBasic')
api.add_resource(FetchProblems, '/fetchProblems')
api.add_resource(MarkPractice, '/markPractice')
api.add_resource(SavePracticeDraft, '/savePracticeDraft')

api.add_resource(CreateCourse, '/createCourse')
api.add_resource(CreateTopic, '/createTopic')
api.add_resource(CreateSection, '/createSection')
api.add_resource(CourseTitle, '/courseTitle')
api.add_resource(EditCourse, '/editCourse')
api.add_resource(TopicTitle, '/topicTitle')
api.add_resource(EditTopic, '/editTopic')
api.add_resource(EditSection, '/editSection')
api.add_resource(VideoUpload, '/videoUpload')
api.add_resource(CreateMdFile, '/createMdFile')
api.add_resource(PicUpload, '/picUpload')
api.add_resource(CourseDetail, '/courseDetail')
api.add_resource(SectionDetail, '/sectionDetail')
api.add_resource(StudentProcessCourse, '/studentProcessCourse')
api.add_resource(TeacherCourseList, '/teacherCourseList')
api.add_resource(StudentCourseList, '/studentCourseList')
api.add_resource(SectionList, '/sectionList')
api.add_resource(UpdateSectionProcess, '/updateSectionProcess')
api.add_resource(StudentNameList, '/studentNameList')
api.add_resource(ImportStudent, '/importStudent')

api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)
