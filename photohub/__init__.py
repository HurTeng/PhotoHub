# coding=utf-8
from flask import Flask


# 创建应用
def create_app(config):
    # 初始化flask
    app = Flask(__name__)
    app.config.from_object(config)
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

    # 初始化数据库
    from photohub.extensions.flasksqlalchemy import db
    db.init_app(app)

    # 初始化logger
    from photohub.logger import init_logger
    init_logger(app)

    # 初始化
    from photohub.controllers.comic import bp_comic
    app.register_blueprint(bp_comic)

    from photohub.controllers.admin import bp_admin
    app.register_blueprint(bp_admin)

    from photohub.controllers.error import bp_error
    app.register_blueprint(bp_error)

    # 初始化调度器
    from photohub.schedulers.scheduler import init_scheduler
    init_scheduler(app)

    # 创建数据库
    with app.app_context():
        db.create_all()
    return app
