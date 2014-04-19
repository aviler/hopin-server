# -*- coding: utf-8 -*-

# Import CherryPy
import cherrypy
from cherrypy.process.plugins import Daemonizer

from api.config import Config
from api.alive import Alive
from auth import check_password
from db.saplugin import SAEnginePlugin
from db.satool import SATool

if __name__ == '__main__':

    Daemonizer(cherrypy.engine).subscribe()

    # Initialize SQLAlchemy plugin and tool
    SAEnginePlugin(cherrypy.engine).subscribe()
    cherrypy.tools.db = SATool()

    # Mount the CONFIG application
    cherrypy.tree.mount( Config(), '/config',
        {'/' : {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'api.hopin.com.br',
            'tools.auth_basic.checkpassword': check_password,
            'tools.db.on': True}
        }
    )

    # Mount the ALIVE application
    cherrypy.tree.mount( Alive(), '/alive',
        {'/' : {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.auth_basic.on': True,
            'tools.auth_basic.realm': 'api.hopin.com.br',
            'tools.auth_basic.checkpassword': check_password,
            'tools.db.on': True}
        }
    )

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    server.socket_port = 8080
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'api/ssl/certificate.crt'
    # server.ssl_private_key       = 'api/ssl/privateKey.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    # Example for a 2nd server (same steps as above):
    # Remember to use a different port

    # server2             = cherrypy._cpserver.Server()

    # server2.socket_host = "0.0.0.0"
    # server2.socket_port = 8081
    # server2.thread_pool = 30
    # server2.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()
