# -*- coding: utf-8 -*-
from flask import request
from flask.ext.restful import Resource
from uuid import uuid4
from dbop import Mysql
import json

class TestReverseProxy(Resource):
    def get(self):
        
        return {
            "success": True
        }
