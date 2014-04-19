# -*- coding: utf-8 -*-

import cherrypy
from db.user import User

class Alive:

    exposed = True

    def PUT(self, time):

        print("time:  " + time)

        session = cherrypy.request.db
        query = session.query(User).filter(User.email==cherrypy.request.login)
        u = query.first()

        u.minetime = u.minetime + long(time)

        return '''{ "hopins":" ''' + str(u.minetime) + '''" }'''
