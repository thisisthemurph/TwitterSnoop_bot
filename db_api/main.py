from flask import Flask
from flask_restful import Api

from constants import DB_API_HOST, DB_API_PORT
from routes.handle_routes import handle_routes
from routes.watcher_routes import watcher_routes

app = Flask("TwitterSnoop_DB_Api")
app.register_blueprint(handle_routes)
app.register_blueprint(watcher_routes)
api = Api(app)

if __name__ == "__main__":
    app.run(host=DB_API_HOST, port=DB_API_PORT)
