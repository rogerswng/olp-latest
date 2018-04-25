# -*- coding: utf-8 -*-

from flask import request
from flask.ext.restful import Resource
from uuid import uuid4

tableCourse = {}
# courseId: {courseTitle, courseDescription, teacherId}
tableCourseStudent = {}
#
tableCourseTeacher = {}
# userId: List<courseId>
tableTopicCourse = {}
# courseId: List<topicId>, topicId: {courseId, topicTitle}


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

        if userId in tableCourseTeacher :
            tableCourseTeacher[userId].append(courseId)
        else :
            tableCourseTeacher[userId] = [courseId, ]

        tableCourse[courseId] = {
            'courseTitle': courseTitle,
            'courseDescription': courseDescription,
            'teacherId': userId
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
        # data = request.args.get("userId")
        userId = request.args.get("userId")
        character = request.args.get("character")

        respData = {}
        courseList = tableCourseTeacher[userId]
        courseDetail = []
        courseCount = len(courseList)
        for i in range(0, courseCount):
            courseId = courseList[i]
            topicIdList = tableTopicCourse[courseId]
            topicList = list(map(lambda x: tableTopicCourse[x]['topicTitle'], topicIdList))
            cd = {
                "title": tableCourse[courseId]['courseTitle'],
                "count": len(tableTopicCourse[courseId]),
                "topicList": topicList
            }
            courseDetail.append(cd)

        respData = {
            "count": courseCount,
            "courses": courseDetail
        }

        return respData

class StudentCourseList(Resource):
    # Fetch Student Course List
    def get(self):
        userId = request.args.get("userId")
        character = request.args.get("character")

        respData = {}
        courseList = tableCourseTeacher[userId]
        courseDetail = []
        courseCount = len(courseList)
        for i in range(0, courseCount) :
            courseId = courseList[i]
            courseTitle = tableCourse[courseId]['courseTitle']
            courseDescription = tableCourse[courseId]['courseDescription']
            teacherId = tableCourse[courseId]['teacherId']
            cd = {
                "title": courseTitle,
                "description": courseDescription,
                "id": courseId,
                "teacher": teacherId
            }
            courseDetail.append(cd)

        respData = {
            "count": courseCount,
            "courses": courseDetail
        }
        return respData
