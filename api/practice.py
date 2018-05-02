# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource
from uuid import uuid4
from app import db
import snowflake.client

# -*- API LIST -*-

#

def get_id():
    return snowflake.client.get_guid()

class TeacherPracticeList(Resource):
    def get(self):
        userId = request.args.get("userId")

        practiceCount = db.getOne(
            """
            select practice_count from User where user_id=%s;
            """,
            (userId,)
        )['practice_count']

        if practiceCount <= 5:
            page = 0
            res = db.getAll(
                """
                select * from Practice where teacher_id=%s;
                """
            )
