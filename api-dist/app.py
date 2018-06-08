from flask import Flask, Response
from flask_restful import Api, Resource
from flask_cors import CORS
# from dbop import Mysql

# Database Connector Pool Initialize
# db = Mysql()

application = app = Flask(__name__, static_folder='statics')
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
from practice import TeacherCourse, TeacherTopic, TeacherSection
from login import Login
from testreverseproxy import TestReverseProxy

api.add_resource(TestReverseProxy, '/api/testReverseProxy')

api.add_resource(TeacherSection, '/api/teacherSection')
api.add_resource(TeacherTopic, '/api/teacherTopic')
api.add_resource(TeacherCourse, '/api/teacherCourse')
api.add_resource(CreatePractice, '/api/createPractice')
api.add_resource(EditPractice, '/api/editPractice')
api.add_resource(CreateProblem, '/api/createProblem')
api.add_resource(EditProblem, '/api/editProblem')
api.add_resource(StudentPracticeList, '/api/studentPracticeList')
api.add_resource(TeacherPracticeList, '/api/teacherPracticeList')
api.add_resource(PracticeBasic, '/api/practiceBasic')
api.add_resource(FetchProblems, '/api/fetchProblems')
api.add_resource(MarkPractice, '/api/markPractice')
api.add_resource(SavePracticeDraft, '/api/savePracticeDraft')

api.add_resource(CreateCourse, '/api/createCourse')
api.add_resource(CreateTopic, '/api/createTopic')
api.add_resource(CreateSection, '/api/createSection')
api.add_resource(CourseTitle, '/api/courseTitle')
api.add_resource(EditCourse, '/api/editCourse')
api.add_resource(TopicTitle, '/api/topicTitle')
api.add_resource(EditTopic, '/api/editTopic')
api.add_resource(EditSection, '/api/editSection')
api.add_resource(VideoUpload, '/api/videoUpload')
api.add_resource(CreateMdFile, '/api/createMdFile')
api.add_resource(PicUpload, '/api/picUpload')
api.add_resource(CourseDetail, '/api/courseDetail')
api.add_resource(SectionDetail, '/api/sectionDetail')
api.add_resource(StudentProcessCourse, '/api/studentProcessCourse')
api.add_resource(TeacherCourseList, '/api/teacherCourseList')
api.add_resource(StudentCourseList, '/api/studentCourseList')
api.add_resource(SectionList, '/api/sectionList')
api.add_resource(UpdateSectionProcess, '/api/updateSectionProcess')
api.add_resource(StudentNameList, '/api/studentNameList')
api.add_resource(ImportStudent, '/api/importStudent')

api.add_resource(Login, '/api/login')

if __name__ == '__main__':
    app.run(debug=True)
