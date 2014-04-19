# -*- coding: utf-8 -*-

import cherrypy
from db.user import User

def check_password(realm, user, password):

    session = cherrypy.request.db
    query = session.query(User).filter(User.email==user)
    u = query.first()

    if u.password == password:
        print("Authorized")
        return True
    else:
        print("Not Authorized")
        return False
