# -*- coding: utf-8 -*-

from flask import Request
from flask.ext.restful import Resource
from uuid import uuid4

tableCourse = {}
tableCourseTeacher = {}
tableTopicCourse = {}

class CreateCourse(Resource):
    # 新建课程
    def post(self):
        userId = request.form['userId']
        courseTitle = request.form['courseTitle']
        courseDescription = request.form['courseDescription']
        topicCount = request.form['topics']['count']
        topics = request.form['topics']['details']

        courseId = uuid4()
        tableCourseTeacher['courseId'] = userId
        tableCourse['courseId'] = {
            'courseTitle': courseTitle,
            'courseDescription': courseDescription
        }
        for i in range(0, topicCount):
            topicId = uuid4()
            tableTopicCourse['topicId'] = {
                'courseId': courseId,
                'topicTitle': topics[i]['topicTitle']
            }

        return {
            "courseId": courseId,
            "courseDetail": tableCourse[courseId]
        }, 200, {
            "Access-Control-Allow-Origin": "*"
        }
