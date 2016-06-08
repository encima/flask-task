from app import app, db, models
import csv, sys
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop



if app.config['ENV'] == 'PROD':
    db.create_all()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    print("Running production")
    IOLoop.instance().start()
elif app.config['ENV'] == 'DEV':
    db.drop_all()
    db.create_all()
    print("Running development")
    app.run(debug=True)
