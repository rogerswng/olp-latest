# -*- coding: utf-8 -*-
from flask import request
from flask_restful import Resource
from uuid import uuid4
from dbop import Mysql
import json
# from app import db
import snowflake.client

# -*- API LIST -*-

# GET /api/teacherPracticeList {userId}
# GET /api/studentPracticeList {userId}
# POST /api/createPractice {}

def get_id():
    return snowflake.client.get_guid()

class TeacherCourse(Resource):
    # 练习关联课程获取老师名下所有课程
    def get(self):
        teacherId = int(request.args.get("uid"))

        db = Mysql()

        cl = db.getAll(
            """
            select * from Course where teacher_id=%s;
            """, (teacherId,)
        )
        if not cl:
            return {
                "success": True,
                "courses": []
            }

        courses = []
        for course in cl:
            data = {
                "value": str(course["course_id"]),
                "title": course["title"]
            }
            courses.append(data)

        return {
            "success": True,
            "courses": courses
        }

class TeacherTopic(Resource):
    # 练习关联课程，获取课程下所有章节
    def get(self):
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        tl = db.getAll(
            """
            select * from Topic where course_id=%s;
            """, (courseId,)
        )

        if not tl:
            return {
                "success": True,
                "topics": []
            }

        topics = []
        for topic in tl:
            data = {
                "value": str(topic["topic_id"]),
                "title": topic["title"]
            }
            topics.append(data)

        return {
            "success": True,
            "topics": topics
        }

class TeacherSection(Resource):
    # 练习关联课程，获取章节下所有小节
    def get(self):
        topicId = int(request.args.get("topicId"))

        db = Mysql()

        sl = db.getAll(
            """
            select * from Section where topic_id=%s;
            """, (topicId,)
        )

        if not sl:
            return {
                "success": True,
                "sections": []
            }

        sections = []
        for section in sl:
            data = {
                "value": str(section["section_id"]),
                "title": section["title"]
            }
            sections.append(data)

        return {
            "success": True,
            "sections": sections
        }

class EditProblem(Resource):
    def put(self):
        data = request.get_json() or request.form
        practiceId = int(data["practiceId"])
        problemId = int(data["problemId"])
        position = data["index"]
        content = data["content"]
        choices = data["choices"]
        answer = data["answer"]

        db = Mysql()

        # Edit Problem
        choices = json.dumps(choices)
        db.modify(
            """
            update Problem set position=%s,content=%s,choices=%s,answer=%s where problem_id=%s;
            """, (position,content,choices,answer,problemId)
        )
        # Reset Status of Practice
        sl = db.getAll(
            """
            select student_id from StudentPractice where practice_id=%s;
            """, (practiceId,)
        )
        if sl:
            for student in sl:
                id = student["student_id"]
                db.modify(
                    """
                    update StudentPractice set status=0 where student_id=%s and practice_id=%s;
                    """, (id,practiceId)
                )

        p = db.getAll(
            """
            select * from Problem where practice_id=%s;
            """, (practiceId,)
        )
        pl = []

        for each in p:
            ch = json.loads(each["choices"])
            d = {
                "id": str(each["problem_id"]),
                "problem": each["content"],
                "choices": [{"cid": i, "value": ch[i]} for i in range(0, len(ch))],
                "correctAnswer": each["answer"]
            }
            pl.append(d)

        return {
            "success": True,
            "problemList": pl
        }

    def delete(self):
        problemId = int(request.args.get("problemId"))

        db = Mysql()

        # Get practice
        practiceId = db.getOne(
            """
            select practice_id from Problem where problem_id=%s;
            """, (problemId,)
        )["practice_id"]

        # Delete Problem
        db.delete(
            """
            delete from Problem where problem_id=%s;
            """, (problemId,)
        )

        # Reset Status of Practice
        sl = db.getAll(
            """
            select student_id from StudentPractice where practice_id=%s;
            """, (practiceId,)
        )
        if sl:
            for student in sl:
                id = student["student_id"]
                db.modify(
                    """
                    update StudentPractice set status=0 where student_id=%s and practice_id=%s;
                    """, (id,practiceId)
                )

        p = db.getAll(
            """
            select * from Problem where practice_id=%s;
            """, (practiceId,)
        )
        pl = []

        if p:
            for each in p:
                ch = json.loads(each["choices"])
                d = {
                    "id": str(each["problem_id"]),
                    "problem": each["content"],
                    "choices": [{"cid": i, "value": ch[i]} for i in range(0, len(ch))],
                    "correctAnswer": each["answer"]
                }
                pl.append(d)

        return {
            "success": True,
            "problemList": pl
        }

class CreateProblem(Resource):
    def post(self):
        data = request.get_json() or request.form
        practiceId = int(data["practiceId"])
        position = data["index"]
        content = data["content"]
        choices = data["choices"]
        answer = data["answer"]

        problemId = get_id()

        db = Mysql()

        # Handle choice list -> json str
        choices = json.dumps(choices)

        db.insertOne(
            """
            insert into Problem (`problem_id`,`position`,`content`,`choices`,`answer`,`practice_id`) values (%s,%s,%s,%s,%s,%s);;
            """, (problemId,position,content,choices,answer,practiceId)
        )
        # Get Students list and reset the status of practice
        sl = db.getAll(
            """
            select student_id from StudentPractice where practice_id=%s;
            """, (practiceId,)
        )
        if sl:
            # Has student
            for student in sl:
                id = student["student_id"]
                db.modify(
                    """
                    update StudentPractice set status=0 where practice_id=%s and student_id=%s;
                    """, (practiceId, id)
                )


        p = db.getAll(
            """
            select * from Problem where practice_id=%s;
            """, (practiceId,)
        )
        pl = []

        for each in p:
            ch = json.loads(each["choices"])
            d = {
                "id": str(each["problem_id"]),
                "problem": each["content"],
                "choices": [{"cid": i, "value": ch[i]} for i in range(0, len(ch))],
                "correctAnswer": each["answer"]
            }
            pl.append(d)

        return {
            "success": True,
            "problemList": pl
        }

class EditPractice(Resource):
    def get(self):
        practiceId = int(request.args.get("practiceId"))

        db = Mysql()

        p = db.getOne(
            """
            select * from Practice where practice_id=%s;
            """, (practiceId,)
        )
        relation = p["relation"]
        if relation == 0:
            # course
            coursetitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (p["course_id"],)
            )["title"]
            relation = "{}".format(coursetitle)

        elif relation == 1:
            # course, topic
            coursetitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (p["course_id"],)
            )["title"]
            topictitle = db.getOne(
                """
                select title from Topic where topic_id=%s;
                """, (p["topic_id"],)
            )["title"]
            relation = "{} / {}".format(coursetitle, topictitle)

        elif relation == 2:
            # course, topic, section
            coursetitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (p["course_id"],)
            )["title"]
            topictitle = db.getOne(
                """
                select title from Topic where topic_id=%s;
                """, (p["topic_id"],)
            )["title"]
            sectiontitle = db.getOne(
                """
                select title from Section where section_id=%s;
                """, (p["section_id"],)
            )["title"]
            relation = "{} / {} / {}".format(coursetitle, topictitle, sectiontitle)

        elif relation == 3:
            # no relation
            relation = "暂未关联任何课程"

        problems = db.getAll(
            """
            select * from Problem where practice_id=%s;
            """, (practiceId,)
        )
        pl = []
        if problems:
            # Has Problems
            for each in problems:
                choices = json.loads(each["choices"])
                d = {
                    "id": str(each["problem_id"]),
                    "problem": each["content"],
                    "choices": [{"cid": i, "value": choices[i]} for i in range(0, len(choices))],
                    "correctAnswer": each["answer"]
                }
                pl.append(d)
        else:
            # No Problems
            pl = []

        return {
            "success": True,
            "title": p["title"],
            "problemList": pl,
            "relation": relation
        }

    def put(self):
        data = request.get_json() or request.form
        practiceId = int(data["practiceId"])
        title = data["title"]
        relatedCourse = data["relatedCourse"]
        relatedTopic = data["relatedTopic"]
        relatedSection = data["relatedSection"]

        db = Mysql()

        rl = db.getOne(
            """
            select relation,course_id from Practice where practice_id=%s;
            """, (practiceId,)
        )

        db.modify(
            """
            update Practice set title=%s where practice_id=%s;
            """, (title,practiceId)
        )
        # Relation modify here
        if relatedCourse == "":
            # no change
            pass
        else:
            if relatedSection == "" or relatedSection == "0":
                if relatedTopic == "" or relatedTopic == "0":
                    # relation 0
                    courseId = int(relatedCourse)
                    db.modify(
                        """
                        update Practice set relation=0,course_id=%s where practice_id=%s;
                        """, (courseId, practiceId)
                    )
                else:
                    # relation 1
                    courseId = int(relatedCourse)
                    topicId = int(relatedTopic)
                    db.modify(
                        """
                        update Practice set relation=1,course_id=%s,topic_id=%s where practice_id=%s;
                        """, (courseId, topicId, practiceId)
                    )
            else:
                # relation 2
                courseId = int(relatedCourse)
                topicId = int(relatedTopic)
                sectionId = int(relatedSection)
                db.modify(
                    """
                    update Practice set relation=2,course_id=%s,topic_id=%s,section_id=%s where practice_id=%s;
                    """, (courseId, topicId, sectionId, practiceId)
                )

            # Handle students
            # 删除以前的所有记录
            db.delete(
                """
                delete from StudentPractice where practice_id=%s;
                """, (practiceId,)
            )
            if rl["relation"] != 3:
                courseBefore = rl["course_id"]
                # 以前的课程 -1
                db.modify(
                    """
                    update Course set practice_count=practice_count-1 where course_id=%s;
                    """, (courseBefore,)
                )
            # 新课程 +1
            db.modify(
                """
                update Course set practice_count=practice_count+1 where course_id=%s;
                """, (courseId,)
            )
            # 新增新的课程学生的记录
            sl = db.getAll(
                """
                select student_id from StudentCourse where course_id=%s;
                """, (courseId,)
            )
            if sl:
                for student in sl:
                    db.insertOne(
                        """
                        insert into StudentPractice (`student_id`,`practice_id`,`status`) values (%s,%s,0);
                        """, (student["student_id"],practiceId)
                    )


        return {
            "success": True
        }

class PracticeBasic(Resource):
    def get(self):
        practiceId = int(request.args.get("practiceId"))

        db = Mysql()

        d = db.getOne(
            """
            select * from Practice where practice_id=%s;
            """, (practiceId,)
        )
        print (d)

        d["practice_id"] = str(d["practice_id"])
        d["teacher_id"] = str(d["teacher_id"])

        relation = d["relation"]

        if relation == 0:
            courseTitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (d["course_id"],)
            )["title"]
            d["relation"] = courseTitle
            d["course_id"] = str(d["course_id"])
        elif relation == 1:
            courseTitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (d["course_id"],)
            )["title"]
            topicTitle = db.getOne(
                """
                select title from Topic where topic_id=%s;
                """, (d["topic_id"],)
            )["title"]
            d["relation"] = "{} / {}".format(courseTitle, topicTitle)
            d["course_id"] = str(d["course_id"])
            d["topic_id"] = str(d["topic_id"])
        elif relation == 2:
            courseTitle = db.getOne(
                """
                select title from Course where course_id=%s;
                """, (d["course_id"],)
            )["title"]
            topicTitle = db.getOne(
                """
                select title from Topic where topic_id=%s;
                """, (d["topic_id"],)
            )["title"]
            sectionTitle = db.getOne(
                """
                select title from Section where section_id=%s;
                """, (d["section_id"],)
            )["title"]
            d["relation"] = "{} / {} / {}".format(courseTitle, topicTitle, sectionTitle)
            d["course_id"] = str(d["course_id"])
            d["topic_id"] = str(d["topic_id"])
            d["section_id"] = str(d["section_id"])

        return d

class TeacherPracticeList(Resource):
    def get(self):
        uid = int(request.args.get("uid"))

        db = Mysql()

        p = db.getAll(
            """
            select * from Practice where teacher_id=%s;
            """, (uid,)
        )
        if not p:
            return {
                "success": True,
                "practiceList": []
            }

        pl = []
        for each in p:
            # format relation string
            r = each["relation"]

            if r == 0:
                relation = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (each["course_id"],)
                )["title"]
            elif r == 1:
                courseTitle = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (each["course_id"],)
                )["title"]
                topicTitle = db.getOne(
                    """
                    select title from Topic where topic_id=%s;
                    """, (each["topic_id"],)
                )["title"]
                relation = "{} / {}".format(courseTitle, topicTitle)
            elif r == 2:
                courseTitle = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (each["course_id"],)
                )["title"]
                topicTitle = db.getOne(
                    """
                    select title from Topic where topic_id=%s;
                    """, (each["topic_id"],)
                )["title"]
                sectionTitle = db.getOne(
                    """
                    select title from Section where section_id=%s;
                    """, (each["section_id"],)
                )["title"]
                relation = "{} / {} / {}".format(courseTitle,topicTitle,sectionTitle)
            else:
                relation = ""

            d = {
                "title": each["title"],
                "relation": relation,
                "id": str(each["practice_id"])
            }

            pl.append(d)


        return {
            "success": True,
            "practiceList": pl
        }

class StudentPracticeList(Resource):
    def get(self):
        uid = request.args.get("uid")

        # practiceCount = db.getOne(
        #     """
        #     select practice_count from User where user_id=%s;
        #     """, (userId,)
        # )['practice_count']
        #
        # if practiceCount < 5:
        #     page = 0
        #     res = db.getAll(
        #         """
        #         select * from StudentPractice where student_id=%s;
        #         """, (userId,)
        #     )
        # else:
        #     page = practiceCount/5+1 if practiceCount%5 else practiceCount/5
        #     res = db.getSome(
        #         """
        #         select * from StudentPractice where student_id=%s;
        #         """, 5, (userId,)
        #     )
        db = Mysql()

        # Get practice list
        practices = db.getAll(
            """
            select * from StudentPractice where student_id=%s;
            """, (uid,)
        )

        for practice in practices:
            practiceId = practice["practice_id"]
            practiceInfo = db.getOne(
                """
                select * from Practice where practice_id=%s;
                """,(practiceId,)
            )
            relation = practiceInfo["relation"]

            if relation == 0:
                # related with course
                courseTitle = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (practiceInfo["course_id"],)
                )["title"]
                practiceInfo["relation"] = courseTitle
                practiceInfo["course_id"] = str(practiceInfo["course_id"])
            elif relation == 1:
                # related with topic
                courseTitle = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (practiceInfo["course_id"],)
                )["title"]
                topicTitle = db.getOne(
                    """
                    select title from Topic where topic_id=%s;
                    """, (practiceInfo["topic_id"],)
                )["title"]
                practiceInfo["relation"] = "{} / {}".format(courseTitle, topicTitle)
                practiceInfo["course_id"] = str(practiceInfo["course_id"])
                practiceInfo["topic_id"] = str(practiceInfo["topic_id"])
            elif relation == 2:
                # related with section
                courseTitle = db.getOne(
                    """
                    select title from Course where course_id=%s;
                    """, (practiceInfo["course_id"],)
                )["title"]
                topicTitle = db.getOne(
                    """
                    select title from Topic where topic_id=%s;
                    """, (practiceInfo["topic_id"],)
                )["title"]
                sectionTitle = db.getOne(
                    """
                    select title from Section where section_id=%s;
                    """, (practiceInfo["section_id"],)
                )["title"]
                practiceInfo["relation"] = "{} / {} / {}".format(courseTitle, topicTitle, sectionTitle)
                practiceInfo["course_id"] = str(practiceInfo["course_id"])
                practiceInfo["topic_id"] = str(practiceInfo["topic_id"])
                practiceInfo["section_id"] = str(practiceInfo["section_id"])


            practiceInfo["practice_id"] = str(practiceInfo["practice_id"])
            practiceInfo["teacher_id"] = str(practiceInfo["teacher_id"])

            practice["detail"] = practiceInfo
            practice["practice_id"] = str(practice["practice_id"])
            practice["student_id"] = str(practice["student_id"])


        respData = practices

        return respData


class CreatePractice(Resource):
    def post(self):
        data = request.get_json() or request.form
        userId = int(data["userId"])
        title = data["title"]
        relatedCourse = data["relatedCourse"]
        relatedTopic = data["relatedTopic"]
        relatedSection = data["relatedSection"]

        db = Mysql()

        practiceId = get_id()

        db.insertOne(
            """
            insert into Practice (`practice_id`,`title`,`teacher_id`) values (%s,%s,%s);
            """,(practiceId,title,userId)
        )

        db.modify(
            """
            update User set practice_count=practice_count+1 where user_id=%s;
            """,(userId,)
        )

        if relatedCourse == "" or relatedCourse == "0":
            # relation = 3
            db.modify(
                """
                update Practice set relation=3 where practice_id=%s;
                """, (practiceId,)
            )
        else:
            if relatedSection == "" or relatedSection == "0":
                if relatedTopic == "" or relatedTopic == "0":
                    # relation = 0
                    courseId = int(relatedCourse)
                    db.modify(
                        """
                        update Practice set relation=0,course_id=%s where practice_id=%s;
                        """, (courseId,practiceId)
                    )
                else:
                    # relation = 1
                    courseId = int(relatedCourse)
                    topicId = int(relatedTopic)
                    db.modify(
                        """
                        update Practice set relation=1,course_id=%s,topic_id=%s where practice_id=%s;
                        """, (courseId,topicId,practiceId)
                    )
            else:
                # relation = 2
                courseId = int(relatedCourse)
                topicId = int(relatedTopic)
                sectionId = int(relatedSection)
                db.modify(
                    """
                    update Practice set relation=2,course_id=%s,topic_id=%s,section_id=%s where practice_id=%s;
                    """, (courseId,topicId,sectionId,practiceId)
                )

            # 给课程增加上这个练习 +1
            db.modify(
                """
                update Course set practice_count=practice_count+1 where course_id=%s;
                """, (courseId,)
            )
            # 让所有课程的学生添加上这个练习
            sl = db.getAll(
                """
                select student_id from StudentCourse where course_id=%s;
                """, (courseId,)
            )
            if sl:
                for student in sl:
                    db.insertOne(
                        """
                        insert into StudentPractice (`student_id`,`practice_id`,`status`) values (%s,%s,0);
                        """, (student["student_id"],practiceId)
                    )

        return {
            "state": "success",
            "id": str(practiceId)
        }

# class CreatePractice(Resource):
#     def post(self):
#         data = request.get_json() or request.form
#         userId = data['userId']
#         title = data['title']
#         problemList = data['problems']
#         relation = data['relation']
#         topicId = data['topicId']
#         sectionId = data['sectionId']
#         courseId = data['courseId']
#
#         practiceId = get_id()
#
#         db.insertOne(
#             """
#             insert into Practice (practice_id, title, teacher_id, relation, topic_id, section_id, course_id)
#             values (%s, %s, %s, %s, %s, %s, %s);
#             """, (practiceId, title, userId, relation, topicId, sectionId, courseId)
#         )
#
#         position = 0
#
#         for eachp in problemList:
#             problemId = get_id()
#
#             content = eachp['content']
#             choices = eachp['choices']
#             answer = eachp['answer']
#
#             db.insertOne(
#                 """
#                 insert into Problem (problem_id, position, content, choices, answer, practice_id)
#                 values (%s, %s, %s, %s, %s, %s);
#                 """, (problemId, position, content, choices, answer, practiceId)
#             )
#
#             position += 1
#
#         studentList = db.getAll(
#             """
#             select student_id from StudnetCourse where course_id=%s;
#             """, (courseId)
#         )
#
#         for each in studentList:
#             db.insertOne(
#                 """
#                 insert into StudentPractice (student_id, practice_id, status)
#                 values (%s, %s, %s);
#                 """, (each['student_id'], practiceId, 0)
#             )
#             db.modify(
#                 """
#                 update User set practice_count=practice_count+1 where user_id=%s;
#                 """, (each['student_id'],)
#             )
#
#         return {
#             "state": "success"
#         }

class FetchProblems(Resource):
    def get(self):
        practiceId = request.args.get('practiceId')
        uid = request.args.get("uid")

        db = Mysql()

        draft = db.getOne(
            """
            select * from StudentPractice where student_id=%s and practice_id=%s;
            """, (uid, practiceId)
        )
        problemSet = db.getAll(
            """
            select problem_id as id, position, content, choices from Problem where practice_id=%s;
            """, (practiceId,)
        )

        status = draft["status"]
        # problemSet["status"] = status

        if status == 0:
            for problem in problemSet:
                problem["status"] = 0
                problem["choices"] = json.loads(problem["choices"])
                problem["id"] = str(problem["id"])
        elif status == 1:
            d = eval(draft["draft"])
            for problem in problemSet:
                id = problem["id"]
                problem["status"] = 1
                problem["choices"] = json.loads(problem["choices"])
                problem["draft"] = d[id]
                problem["id"] = str(problem["id"])
        elif status == 2:
            d = eval(draft["draft"])
            for problem in problemSet:
                id = problem["id"]
                problem["status"] = 2
                problem["choices"] = json.loads(problem["choices"])
                problem["draft"] = d[id]
                answer = db.getOne(
                    """
                    select answer from Problem where problem_id=%s;
                    """, (problem["id"],)
                )["answer"]
                problem["correctAnswer"] = problem["choices"].index(answer)
                problem["id"] = str(problem["id"])

        respData = {
            "problemSet":problemSet,
            "status": status
        }

        return respData

class UploadPractice(Resource):
    def post(self):
        data = request.get_json() or request.form
        userId = data['userId']
        detail = data['detail']
        duration = data['duration']

        correctCount = 0

        for each in detail:
            problemId = each['problemId']
            answer = each['answer']

            correctAnswer = db.getOne(
                """
                select answer from Problem where problem_id=%s;
                """, (problemId,)
            )

            if answer == correctAnswer:
                each['status'] = True
                correctCount += 1
            else:
                each['status'] = False

            each['correctAnswer'] = correctAnswer

        db.modify(
            """
            update StudentPractice set status=%s, draft=%s, score=%s, duration=%s where student_id=%s and practice_id=%s;
            """, (2, detail, correctCount, duration, userId, practiceId)
        )

        respData = {
            "state": "success",
            "detail": detail,
            "score": correctCount
        }

        return respData

class MarkPractice(Resource):
    def post(self):
        data = request.get_json() or request.form
        uid = int(data["uid"])
        practiceId = int(data["practiceId"])
        p = data["problems"]

        db = Mysql()

        # Get correct answer list
        d = db.getAll(
            """
            select problem_id as id, answer, choices from Problem where practice_id=%s;
            """, (practiceId,)
        )
        cl = {}
        for problem in d:
            problem["choices"] = json.loads(problem["choices"])
            # value not index
            cl[problem["id"]] = problem["choices"].index(problem["answer"])

        # Handle format of post data & save draft into a dict
        draft = {}
        for problem in p:
            pid = int(problem["id"])
            problem["status"] = 2
            problem["correctAnswer"] = cl[pid]
            draft[pid] = problem["draft"]

        db.modify(
            """
            update StudentPractice set status=2,draft=%s where student_id=%s and practice_id=%s;
            """, (str(draft),uid,practiceId)
        )

        return p


class SavePracticeDraft(Resource):
    def post(self):
        data = request.get_json() or request.form
        uid = int(data["uid"])
        practiceId = int(data["practiceId"])
        p = data["problems"]

        db = Mysql()

        drafts = {}
        for problem in p:
            pid = int(problem["id"])
            if "draft" in problem:
                drafts[pid] = problem["draft"]
            else:
                drafts[pid] = None

        db.modify(
            """
            update StudentPractice set status=1,draft=%s where student_id=%s and practice_id=%s;
            """, (str(drafts),uid,practiceId)
        )

        return {"success": True}
