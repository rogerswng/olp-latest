# -*- coding: utf-8 -*-

from flask import request
from flask.ext.restful import Resource
from uuid import uuid4

tableCourse = {}
tableCourseStudent = {}
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
        tableCourseTeacher[userId] = []
        tableCourseTeacher[userId].append(courseId)
        tableCourse[courseId] = {
            'courseTitle': courseTitle,
            'courseDescription': courseDescription
        }
        tableTopicCourse[courseId] = []
        for i in range(0, topicCount):
            topicId = str(uuid4())
            tableTopicCourse[courseId].append(topicId)
            tableTopicCourse[topicId] = {
                'courseId': courseId,
                'topicTitle': topics[i]['topicTitle']
            }
        respData = {
            "courseId": courseId,
            "courseDetail": tableCourse[courseId]
        }
        return respData

class TeacherCourseList(Resource):
    # Fetch 课程列表
    def get(self):
        data = request.get_json() or request.form
        return data
        # userId = data['userId']
        # character = data['character']
        #
        # respData = {}
        # courseList = tableCourseTeacher[userId]
        # courseDetail = []
        # courseCount = len(courseList)
        # for i in range(0, courseCount):
        #     courseId = courseList[i]
        #     topicIdList = tableTopicCourse[courseId]
        #     topicList = map(lambda x: tableTopicCourse[x]['topicTitle'], topicIdList)
        #     cd = {
        #         "title": tableCourse[courseId]['courseTitle'],
        #         "count": len(tableTopicCourse[courseId]),
        #         "topicList": topicList
        #     }
        #     courseDetail.append(cd)
        #
        # respData = {
        #     "count": courseCount,
        #     "courses": courseDetail
        # }
        #
        # return respData
