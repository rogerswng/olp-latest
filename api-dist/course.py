# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from uuid import uuid4
from dbop import Mysql
from os import path
from werkzeug.utils import secure_filename
# from app import db
import json
import snowflake.client

# -*- API LIST -*-

# POST /api/createCourse {userId, courseTitle, courseDescription, topicCount, topics{topicTitle}}
# PUT /api/editCourse {courseId, title, description}
# GET /api/envalidCourse {state, courseId}
# GET /api/teacherCourseList {userId, character}
# GET /api/studentCourseList {userId, character}
# POST /api/editTopic {courseId, title}
# PUT /api/editTopic {topicId, title}
# DELETE /api/editTopic {topicId}
# POST /api/editSection {userId, courseId, topicId, sectionTitle, entityType, entityId}
# PUT /api/editSection {userId, courseId, topicId, sectionTitle, entityType, entityId}
# DELETE /api/editSection {sectionId}
# POST /api/importStudent {importType, courseId, students{id:school_id}}
# GET /api/sectionList {userId, courseId}
# POST /api/updateSectionProcess

def get_id():
    return snowflake.client.get_guid()

class CreateMdFile(Resource):
    # 后端存储 markdown 源代码，以.md文件的形式存储
    def post(self):
        data = request.get_json() or request.form
        md = data["md"]

        fid = get_id()
        filename = "{}doc.md".format(str(fid))
        base_path = path.abspath(path.dirname(__file__))
        des_path = path.join(base_path, 'statics/md/')
        file_name = des_path+secure_filename(filename)
        with open(file_name, 'w') as f:
            f.write(md)
            f.close()

        return {
            "success": True,
            "url": "http://58.87.72.44:80/statics/md/"+secure_filename(filename)
        }


class StudentNameList(Resource):
    # 获取某课程的学生名单
    def get(self):
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        # Get Student List
        d = db.getAll(
            """
            select student_id from StudentCourse where course_id=%s;
            """, (courseId,)
        )
        students = []
        i = 0
        if not d:
            return students

        for each in d:
            studentId = db.getOne(
                """
                select school_id from User where user_id=%s;
                """, (each["student_id"],)
            )["school_id"]
            students.append({"number": i,"uid":str(studentId)})
            i += 1

        return students

class ImportStudent(Resource):
    def post(self):
        data = request.get_json() or request.form

        courseId = int(data["courseId"])
        uid = int(data["uid"])

        db = Mysql()

        # Check if the student is exists
        d = db.getOne(
            """
            select `user_id`,`character` from User where school_id=%s;
            """, (uid,)
        )
        if d and d["character"]==0:
            uid = d["user_id"]
        else:
            return {
                "success": False,
                "reason": "此学生不存在，请检查学号是否输入正确！"
            }

        # Initialize course learning process
        # Get Section List first
        t = db.getAll(
            """
            select topic_id from Topic where course_id=%s;
            """, (courseId,)
        )
        sections = {}
        if t:
            for topic in t:
                tid = topic["topic_id"]
                # Get Section List
                sl = db.getAll(
                    """
                    select section_id from Section where topic_id=%s;
                    """, (tid,)
                )
                if sl:
                    for section in sl:
                        sections[str(section["section_id"])] = 0


        # Write Data
        db.insertOne(
            """
            insert into StudentCourse (`student_id`,`course_id`,`status`,`process_detail`) values (%s,%s,0,%s);
            """, (uid,courseId,str(sections))
        )
        db.modify(
            """
            update User set course_count=course_count+1 where user_id=%s;
            """, (uid,)
        )
        db.modify(
            """
            update Course set student_count=student_count+1 where course_id=%s;
            """, (courseId,)
        )

        return {
            "success": True
        }

class UpdateSectionProcess(Resource):
    def post(self):
        data = request.get_json() or request.form

        courseId = int(data["courseId"])
        sectionId = data["sectionId"]
        uid = int(data["uid"])

        db = Mysql()

        # Get current process
        curProcess = db.getOne(
            """
            select process_detail from StudentCourse where student_id=%s and course_id=%s;
            """, (uid,courseId)
        )["process_detail"]

        if not curProcess:
            curProcess = {}
        elif curProcess:
            curProcess = eval(curProcess)

        # Change the Status
        curProcess[sectionId] = 1
        db.modify(
            """
            update StudentCourse set process_detail=%s,last_section_id=%s where student_id=%s and course_id=%s;
            """, (str(curProcess),sectionId,uid,courseId)
        )

        return {"success": True};

class SectionDetail(Resource):
    def get(self):
        sectionId = int(request.args.get("sectionId"))
        studentId = int(request.args.get("uid"))

        db = Mysql()
        res = db.getOne(
            """
            select * from Section where section_id=%s;
            """, (sectionId,)
        )

        if res:
            entityId = res["entity_id"]
            topicId = res["topic_id"]
            entity = db.getOne(
                """
                select * from Entity where entity_id=%s;
                """, (entityId,)
            )
            courseId = db.getOne(
                """
                select course_id from Topic where topic_id=%s;
                """, (topicId,)
            )["course_id"]
            process = db.getOne(
                """
                select process_detail from StudentCourse where course_id=%s and student_id=%s;
                """, (courseId,studentId)
            )["process_detail"]
            process = eval(process)
            status = process[str(sectionId)]

            return {
                "id": str(res["section_id"]),
                "relatedCourse": str(courseId),
                "relatedTopic": str(topicId),
                "entity": {
                    "id": str(entityId),
                    "type": entity["entity_type"],
                    "url": entity["url"],
                    "content": entity["content"]
                },
                "status": status
            }


class VideoUpload(Resource):
    # Section Video Upload
    def post(self):
        f = request.files["file"]
        if f:
            base_path = path.abspath(path.dirname(__file__))
            des_path = path.join(base_path, 'statics/videos/')
            fname = str(get_id())+f.filename
            file_name = des_path+secure_filename(fname)
            f.save(file_name)
            return {
                "state": "success",
                "url": "http://58.87.72.44:80/statics/videos/"+secure_filename(fname)
            }

class PicUpload(Resource):
    # Section Pic Upload
    def post(self):
        f = request.files.get("editormd-image-file")
        if f:
            base_path = path.abspath(path.dirname(__file__))
            des_path = path.join(base_path, 'static/pics/')
            fname = str(get_id())+f.filename
            file_name = des_path+secure_filename(fname)
            f.save(file_name)
            return {
                "success": 1,
                "message": "Success!",
                "url": "http://localhost:8000/static/pics/"+secure_filename(fname)
            }
        else:
            return {
                "success": 0,
                "message": "Not File!"
            }

class CourseTitle(Resource):
    # Teacher get Course Title via courseId
    def get(self):
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        title = db.getOne(
            """
            select title from Course where course_id=%s;
            """, (courseId,)
        )

        if title:
            db.close()
            return title

class TopicTitle(Resource):
    # get topic title
    def get(self):
        topicId = int(request.args.get("topicId"))

        db = Mysql()

        title = db.getOne(
            """
            select title from Topic where topic_id=%s;
            """, (topicId,)
        )

        if title:
            db.close()
            return title

class CourseDetail(Resource):
    # 获取课程详情
    def get(self):
        courseId = int(request.args.get("courseId"))
        studentId = int(request.args.get("studentId"))

        db = Mysql()

        res = db.getOne(
            """
            select * from Course where course_id=%s;
            """, (courseId,)
        )

        d = db.getOne(
            """
            select process_detail from StudentCourse where course_id=%s and student_id=%s;
            """, (courseId, studentId)
        )
        t = db.getOne(
            """
            select name from User where user_id=%s;
            """, (res["teacher_id"])
        )

        processDetail = eval(d["process_detail"])

        resp = {}
        if res:
            resp = {
                "title": res["title"],
                "desc": res["description"],
                "teacher": t["name"]
            }

            if res["topic_count"] != 0:
                topics = db.getAll(
                    """
                    select * from Topic where course_id=%s;
                    """,(courseId,)
                )
                if topics:
                    for topic in topics:
                        sections = []
                        s = db.getAll(
                            """
                            select * from Section where topic_id=%s;
                            """,(topic["topic_id"],)
                        )
                        print (s)
                        if s:
                            for section in s:
                                section["section_id"] = str(section["section_id"])
                                section["topic_id"] = str(section["topic_id"])
                                section["process"] = processDetail[section["section_id"]]
                            sections = s
                        else:
                            sections = []

                        topic["sections"] = sections
                        topic["course_id"] = str(topic["course_id"])
                        topic["topic_id"] = str(topic["topic_id"])
            else:
                topics = []

            resp["topics"] = topics
            resp["id"] = str(courseId)

            db.close()
            return resp

class StudentProcessCourse(Resource):
    # Get the learning process of course
    def get(self):
        courseId = request.args.get("courseId")
        studentId = request.args.get("studentId")

        db = Mysql()

        d = db.getOne(
            """
            select process_detail from StudentCourse where course_id=%s and student_id=%s;
            """, (courseId, studentId)
        )

        processDetail = eval(d["process_detail"])

        return {
            "process": processDetail
        }


        # if

class CreateCourse(Resource):
    # 新建课程
    def post(self):
        """
            POST /api/createCourse
        """

        # Deal with request.data

        data = request.get_json() or request.form
        userId = int(data['userId'])
        print (userId)
        courseTitle = data['courseTitle']
        courseDescription = data['courseDescription']
        # topicCount = data['topics']['count']
        # topics = data['topics']['details']

        # Generate course_id
        courseId = get_id()
        respData = {}

        db = Mysql()


        # SQL Statements
        db.insertOne(
            """
            insert into Course (`course_id`,`title`,`description`,`teacher_id`,`is_valid`)
            values
            (%s, %s, %s, %s, %s);
            """,
            (courseId, courseTitle, courseDescription, userId, 0)
        )
        # res = db.getOne(
        #     """
        #     select * from Course where course_id=%s;
        #     """,(courseId,)
        # )

        # res = db.getOne(
        #     """
        #     select course_count from User where user_id=%s;
        #     """,
        #     (userId,)
        # )
        # if res:
        #     courseCount = res['course_count']+1
        #     db.modify(
        #         """
        #         update User set course_count=%s where user_id=%s;
        #         """,
        #         (courseCount, userId)
        #     )
        db.modify(
            """
            update User set course_count=course_count+1 where user_id=%s;
            """, (userId,)
        )

        respData = {
            "status": True,
            "course_id": str(courseId)
            # "data": res
        }

        db.close()

        return respData

class CreateTopic(Resource):
    # 创建新章节
    def post(self):
        data = request.get_json() or request.form
        courseId = int(data['courseId'])
        title = data['title']

        db = Mysql()

        topicid = get_id()

        db.insertOne(
        """
        insert into Topic (`topic_id`, `title`, `course_id`, `section_count`) values(%s, %s, %s, %s);
        """,(topicid, title, courseId, 0)
        )

        db.modify(
        """
        update Course set topic_count=topic_count+1 where course_id=%s;
        """, (courseId,)
        )

        db.close()

        return {
            "state": "success",
            "topic_id": str(topicid)
        }

class CreateSection(Resource):
    # Create Section
    def post(self):
        data = request.get_json() or request.form
        courseId = int(data['courseId'])
        topicId = int(data['topicId'])
        title = data['title']
        type = data['entity']['entityType']

        db = Mysql()
        sectionId = get_id()

        if type == 'doc':
            db.insertOne(
                """
                insert into Section (`section_id`, `title`, `topic_id`, `entity_type`) values(%s,%s,%s,%s);
                """,(sectionId,title,topicId,1)
            )
            entityId = get_id()
            db.modify(
                """
                update Section set entity_id=%s where section_id=%s;
                """,(entityId, sectionId)
            )
            db.insertOne(
                """
                insert into Entity (`entity_id`, `entity_type`, `content`, `section_id`, `url`) values (%s,%s,%s,%s,%s);
                """, (entityId, 1, data['entity']['content'], sectionId, data['entity']["url"])
            )
        elif type == 'video':
            db.insertOne(
                """
                insert into Section (`section_id`,`title`,`topic_id`,`entity_type`) values(%s,%s,%s,%s);
                """, (sectionId,title,topicId,0)
            )
            entityId = get_id()
            db.modify(
                """
                update Section set entity_id=%s where section_id=%s;
                """, (entityId, sectionId)
            )
            db.insertOne(
                """
                insert into Entity (`entity_id`, `entity_type`, `url`, `section_id`) values (%s,%s,%s,%s);
                """, (entityId, 0, data['entity']['url'], sectionId)
            )

        db.modify(
            """
            update Topic set section_count=section_count+1 where topic_id=%s;
            """, (topicId,)
        )
        db.modify(
            """
            update Course set section_count=section_count+1 where course_id=%s;
            """, (courseId,)
        )

        # Modify process_detail
        pd = db.getAll(
            """
            select `student_id`,`process_detail` from StudentCourse where course_id=%s;
            """, (courseId,)
        )
        if pd:
            for each in pd:
                process = eval(each["process_detail"])
                process[str(sectionId)] = 0
                db.modify(
                    """
                    update StudentCourse set process_detail=%s where course_id=%s and student_id=%s;
                    """,(str(process),courseId,each["student_id"])
                )

        return {
            "state": "success"
        }

class EditCourse(Resource):
    # Edit course
    def get(self):
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        # Get Course Info
        d = db.getOne(
            """
            select `title`,`description` from Course where course_id=%s;
            """, (courseId,)
        )
        t = db.getAll(
            """
            select topic_id as id, title as topicTitle from Topic where course_id=%s;
            """, (courseId,)
        )
        if t:
            for topic in t:
                sl = db.getAll(
                    """
                    select section_id as id, title as sectionTitle, entity_type as entityType from Section where topic_id=%s;
                    """, (topic["id"],)
                )
                if sl:
                    for section in sl:
                        section["id"] = str(section["id"])
                else:
                    sl = []

                topic["sections"] = sl
                topic["id"] = str(topic["id"])
        else :
            t = []

        respData = {
            "id": str(courseId),
            "title": d["title"],
            "desc": d["description"],
            "courseDetail": t
        }

        return respData

    def put(self):
        data = request.get_json() or request.form
        courseId = int(data['courseId'])
        title = data['title']
        desc = data['desc']

        db = Mysql()

        db.modify(
            """
            update Course set title=%s, description=%s where course_id=%s;
            """,
            (title, desc, courseId)
        )

        return {
            "state": "success"
        }

class EnvalidCourse(Resource):
    # 上线/下线课程
    def get(self):
        state = request.args.get("state")
        courseId = request.args.get("courseId")

        cur = 1 if state == False else 0

        db.modify(
            """
            update Course set is_valid=%s where course_id=%s;
            """,
            (cur, courseId)
        )

        return {
            "state": "success",
            "cur": True if cur == 1 else False
        }

class TeacherCourseList(Resource):
    # Fetch 课程列表
    def get(self):
        # data = request.args.get("userId")
        userId = request.args.get("userId")
        # character = request.args.get("character")
        db = Mysql()
        # Query Statements
        res = db.getOne(
            """
            select course_count from User where user_id=%s;
            """,
            (userId,)
        )['course_count']
        if res:
            if res <= 5:
                page = 0
                courseRes = db.getAll(
                    """
                    select * from Course where teacher_id=%s;
                    """,
                    (userId,)
                )
                courseCount = res
            else:
                page = res/5+1 if res%5 else res/5
                courseRes = db.getSome(
                    """
                    select * from Course where teacher_id=%s;
                    """,
                    5, (userId,)
                )
                courseCount = 5

        courseDetail = []
        for i in range(0, courseCount):
            courseDetail.append({
                "id": str(courseRes[i]["course_id"]),
                "title": courseRes[i]['title'],
                "count": [courseRes[i]['topic_count'], courseRes[i]['section_count'], courseRes[i]['practice_count'], courseRes[i]['student_count']]
            })

        respData = {
            "state": "success",
            "count": courseCount,
            "page": page,
            "courses": courseDetail
        }
        db.close()
        return respData

class StudentCourseList(Resource):
    # Fetch Student Course List
    def get(self):
        print ("Get the Request!")
        userId = request.args.get("userId")
        # character = request.args.get("character")
        db = Mysql()

        # Query Statements
        res = db.getOne(
            """
            select course_count from User where user_id=%s;
            """,
            (userId,)
        )['course_count']

        if res:
            if res <= 5:
                page = 0
                # courseRes = db.getAll(
                #     """
                #     select * from Course where course_id in (
                #         select course_id from StudentCourse where student_id=%s
                #     );
                #     """,
                #     (userId,)
                # )
                # User JOIN instead of Sub-query --> faster
                courseRes = db.getAll(
                    """
                    select a.*, b.status, b.last_section_id from Course a inner join StudentCourse b
                    on a.course_id=b.course_id
                    where b.student_id=%s;
                    """,
                    (userId,)
                )
                courseCount = res
            else:
                page = res/5+1 if res%5 else res/5
                courseRes = db.getSome(
                    """
                    select a.*, b.status, b.last_section_id from Course a inner join StudentCourse b
                    on a.course_id=b.course_id
                    where b.student_id=%s;
                    """,
                    5, (userId,)
                )
                courseCount = 5

        courseDetail = []
        for i in range(0, courseCount):
            print (courseRes[i])
            courseId = courseRes[i]['course_id']
            teacherId = courseRes[i]['teacher_id']
            teacherRes = db.getOne(
                """
                select name, icon from User where user_id=%s;
                """,
                (teacherId,)
            )
            if courseRes[i]['last_section_id'] is not None:
                sectionTitle = db.getOne(
                    """
                    select title from Section where section_id=%s;
                    """,
                    (courseRes[i]['last_section_id'],)
                )["title"]
            else:
                sectionTitle = ''

            courseDetail.append({
                "title": courseRes[i]['title'],
                "desc": courseRes[i]['description'],
                "id": str(courseRes[i]['course_id']),
                "teacher": teacherRes["name"],
                "lastProgress": {
                    "title": sectionTitle,
                    "id": str(courseRes[i]['last_section_id'])
                }
            })

        respData = {
            "state": "success",
            "count": courseCount,
            "page": page,
            "courses": courseDetail
        }
        db.close()

        return respData

class EditTopic(Resource):
    # 编辑章节
    def put(self):
        data = request.get_json() or request.form
        topicId = data['topicId']
        title = data['topicTitle']

        db = Mysql()

        db.modify(
            """
            update Topic set title=%s where topic_id=%s;
            """,
            (title, topicId)
        )

        return {
            "success": True
        }

    def delete(self):
        topicId = int(request.args.get("topicId"))
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        # Delete Topic itself
        db.delete(
            """
            delete from Topic where topic_id=%s;
            """,(topicId,)
        )
        db.modify(
            """
            update Practice set relation=3 where topic_id=%s and relation=1;
            """, (topicId,)
        )

        # Get Section list and delete
        sectionIds = db.getAll(
            """
            select section_id as id from Section where topic_id=%s;
            """,(topicId,)
        )
        if sectionIds:
            cnt = len(sectionIds)
            # Delete all sections related with the topic
            db.delete(
                """
                delete from Section where topic_id=%s;
                """,(topicId,)
            )

            # Delete the entities related with sections
            for section in sectionIds:
                id = section["id"]
                db.delete(
                    """
                    delete from Entity where section_id=%s;
                    """,(id,)
                )

            # Untie the relationship of practice
            for section in sectionIds:
                id = section["id"]
                db.modify(
                    """
                    update Practice set relation=3 where section_id=%s and relation=2;
                    """, (id,)
                )

            # Delete the learning process related with deleted sections
            pd = db.getAll(
                """
                select `student_id`,`process_detail` where course_id=%s;
                """, (courseId,)
            )
            if pd:
                for each in pd:
                    process = eval(each["process_detail"])
                    for section in sectionIds:
                        process.pop(str(section["id"]))
                    db.modify(
                        """
                        update StudentCourse set process=detail=%s where student_id=%s and course_id=%s;
                        """, (str(process),each["student_id"],courseId)
                    )

        else :
            cnt = 0

        db.modify(
            """
            update Course set topic_count=topic_count-1, section_count=section_count-%s where course_id=%s;
            """, (cnt, courseId)
        )

        db.close()

        return {
            "state": "success"
        }

class EditSection(Resource):
    # 编辑小节
    def get(self):
        sectionId = int(request.args.get("sectionId"))

        db = Mysql()

        # Get section info and related entity
        s = db.getOne(
            """
            select * from Section where section_id=%s;
            """, (sectionId,)
        )
        entityId = s["entity_id"]
        e = db.getOne(
            """
            select * from Entity where entity_id=%s;
            """, (entityId,)
        )
        respData = {}
        respData["sectionTitle"] = s["title"]
        respData["entity"] = {}
        if s["entity_type"] == 0:
            # video
            respData["entity"]["entityType"] = "video"
            respData["entity"]["url"] = e["url"]
        elif s["entity_type"] == 1:
            # doc
            respData["entity"]["entityType"] = "doc"
            respData["entity"]["url"] = e["url"]
            respData["entity"]["content"] = e["content"]

        return respData

    def put(self):
        data = request.get_json() or request.form
        courseId = int(data['courseId'])
        topicId = int(data['topicId'])
        sectionId = int(data['sectionId'])
        sectionTitle = data['sectionTitle']
        entityType = data['entity']['entityType']
        url = data['entity']['url']

        db = Mysql()
        if entityType == 'video':
            entityType = 0
        elif entityType == 'doc':
            entityType = 1

        # Modify Table Section
        db.modify(
            """
            update Section set title=%s,entity_type=%s where section_id=%s;
            """, (sectionTitle,entityType,sectionId)
        )
        db.modify(
            """
            update Practice set relation=3 where section_id=%s and relation=2;
            """, (sectionId,)
        )
        eid = db.getOne(
            """
            select entity_id from Section where section_id=%s;
            """,(sectionId,)
        )["entity_id"]

        # Modify Entity
        if entityType == 0:
            # video
            db.modify(
                """
                update Entity set entity_type=%s,url=%s where entity_id=%s;
                """, (entityType, url, eid)
            )
        elif entityType == 1:
            # doc
            db.modify(
                """
                update Entity set entity_type=%s,url=%s,content=%s where entity_id=%s;
                """, (entityType, url, data["entity"]["content"], eid)
            )

        return {
            "success": True
        }

    def delete(self):
        sectionId = int(request.args.get('sectionId'))

        db = Mysql()

        # Get Topic and modify section_count
        topicId = db.getOne(
            """
            select topic_id from Section where section_id=%s;
            """, (sectionId,)
        )["topic_id"]
        db.modify(
            """
            update Topic set section_count=section_count-1 where topic_id=%s;
            """, (topicId,)
        )

        # Get Course
        courseId = db.getOne(
            """
            select course_id from Topic where topic_id=%s;
            """, (topicId,)
        )["course_id"]
        db.modify(
            """
            update Course set section_count=section_count-1 where course_id=%s;
            """, (courseId,)
        )

        # Get All Students
        s = db.getAll(
            """
            select `student_id`,`process_detail` from StudentCourse where course_id=%s;
            """, (courseId,)
        )
        if s:
            for student in s:
                pd = eval(student["process_detail"])
                pd.pop(str(sectionId))
                pd = str(pd)
                db.modify(
                    """
                    update StudentCourse set process_detail=%s where student_id=%s;
                    """, (pd,student["student_id"])
                )

        # Delete Section
        db.delete(
            """
            delete from Section where section_id=%s;
            """, (sectionId,)
        )

        return {
            "success": True
        }


class SectionList(Resource):
    # Get Section List in Course Detail Page
    def get(self):
        userId = int(request.args.get("userId"))
        courseId = int(request.args.get("courseId"))

        db = Mysql()

        res = db.getOne(
            """
            select process_detail from StudentCourse where course_id=%s and student_id=%s;
            """, (courseId, userId)
        )["process_detail"]
        sl = db.getAll(
            """
            select * from Section where topic_id in (select topic_id from Topic where course_id=%s);
            """, (courseId,)
        )
        d = []

        if sl:
            res = eval(res)
            for section in sl:
                sectionId = section["section_id"]
                status = res[str(sectionId)]
                d.append({
                    "id": str(sectionId),
                    "title": section["title"],
                    "entity": {
                        "type": section["entity_type"]
                    },
                    "status": status
                })
            # for key, values in res.items():
            #     sectionId = int(key)
            #     status = values
            #
            #     section = db.getOne(
            #         """
            #         select * from Section where section_id=%s;
            #         """, (sectionId)
            #     )
            #     d.append({
            #         "id": key,
            #         "title": section["title"],
            #         "entity": {
            #             "type": section["entity_type"],
            #         },
            #         "status": status
            #     })

        return d
