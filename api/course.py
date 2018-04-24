# -*- coding: utf-8 -*-

from flask import request
from flask.ext.restful import Resource
from uuid import uuid4

tableCourse = {}
tableCourseTeacher = {}
tableTopicCourse = {}

class CreateCourse(Resource):
    # 新建课程
    def post(self):
        data = request.get_json() or request.form
        userId = data['userId']
        courseTitle = data['courseTitle']
        courseDescription = data['courseDescription']
        topicCount = data['topics']['count']
        topics = data['topics']['details']

        courseId = str(uuid4())
        tableCourseTeacher[courseId] = userId
        tableCourse[courseId] = {
            'courseTitle': courseTitle,
            'courseDescription': courseDescription
        }
        for i in range(0, topicCount):
            topicId = str(uuid4())
            tableTopicCourse[topicId] = {
                'courseId': courseId,
                'topicTitle': topics[i]['topicTitle']
            }

        respData = {
            "courseId": courseId,
            "courseDetail": tableCourse[courseId]
        }

        return respData
