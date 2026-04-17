from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'hello'
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///data.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Error handlers
    @app.errorhandler(404)
    def error(er):
        return "قريبا... شكرا لتجربتك متاح حاليا صفحة البوستات والبروفايل فقط", 404

    @app.errorhandler(502)
    def ero502(er):
        return "حصل خطأ هصلحه..", 502

    @app.errorhandler(500)
    def ero500(er):
        return "سجل دخول", 500

    # Blueprints
    from Project.Home import bp as homebp
    from Project.Auth import bp as authbp
    from Project.Profile import bp as profilebp
    from Project.Posts import bp as postsbp
    from Project.admin import bp as adminbp

    app.register_blueprint(authbp)
    app.register_blueprint(homebp)
    app.register_blueprint(profilebp)
    app.register_blueprint(postsbp)
    app.register_blueprint(adminbp)

    with app.app_context():
        db.create_all()

    return app
