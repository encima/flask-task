"""Run the server in either production or development."""
from app import app, db, models
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from passlib.hash import sha256_crypt

if app.config['ENV'] == 'PROD':
    db.create_all()
    email = app.config['ADMIN_EMAIL'].lower()
    pw = app.config['ADMIN_PW']
    hash = sha256_crypt.encrypt(pw)
    user = models.User(email, hash)
    db.session.add(user)
    db.session.commit()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(9000)
    print("Running production on 9000")
    IOLoop.instance().start()
elif app.config['ENV'] == 'DEV':
    db.drop_all()
    db.create_all()
    email = app.config['ADMIN_EMAIL']
    pw = app.config['ADMIN_PW']
    hash = sha256_crypt.encrypt(pw)
    user = models.User(email, hash)
    db.session.add(user)
    db.session.commit()
    print("Running development")
    app.run(debug=True)
