# -*- coding: utf-8 -*-

import cherrypy
from db.user import User

class Config:

    exposed = True

    def GET(self):

        session = cherrypy.request.db
        query = session.query(User).filter(User.email==cherrypy.request.login)
        u = query.first()

        return '''{ "parameters":"''' + u.config + '''" , "hopins":"''' + str(u.minetime) + '''" }'''
