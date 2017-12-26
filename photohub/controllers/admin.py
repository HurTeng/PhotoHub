# coding=utf-8

from flask import Blueprint
from flask import current_app, request, abort, jsonify

import photohub.tasks.task as task


def login():
    # 获取并验证用户名和密码
    valid_user = current_app.config['USERNAME'] == request.args.get('username')
    valid_password = current_app.config['PASSWORD'] == request.args.get('password')
    if not valid_user or not valid_password:
        abort(404)


bp_admin = Blueprint('admin', __name__, url_prefix='/admin')
bp_admin.before_request(login)


@bp_admin.route('/refresh_comics')
def refresh_comics():
    return jsonify(task.refresh_comics())


@bp_admin.route('/refresh_chapters')
def refresh_chapters():
    return jsonify(task.refresh_chapters())


@bp_admin.route('/refresh_comic_images')
def refresh_comic_images():
    return jsonify(task.refresh_comic_images())
