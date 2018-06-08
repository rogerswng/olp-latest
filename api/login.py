# -*- coding: utf-8 -*-

from flask import request
from flask.ext.restful import Resource
from dbop import Mysql
# from app import db

# -*- API LIST -*-
#
# POST /api/login {username, password}
#

class Login(Resource):
    def post(self):
        data = request.get_json() or request.form
        username = data['username']
        password = data['password']

        db = Mysql()

        res = db.getOne(
            """
            select password from User where school_id=%s;
            """, (username,)
        )

        if (res == False):
            db.close()

            return {
                "state": False,
                "reason": "User Not Found."
            }
        elif password == res['password']:
            d = db.getOne(
                """
                select * from User where school_id=%s;
                """, (username,)
            )
            # print(d["user_id"])

            db.close()

            return {
                "state": True,
                "reason": "Success!",
                "data": {
                    "username": username,
                    "character": d['character'],
                    "uid": str(d["user_id"])
                    # "origindata": d
                }
            }
        else:
            db.close()

            return {
                "state": False,
                "reason": "Wrong User/Password."
            }
