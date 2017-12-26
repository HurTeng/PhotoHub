# coding=utf-8

from photohub.models.chapter import Chapter
from photohub.models.comic import Comic
from sqlalchemy import and_


# 获取图片集
def get_comics(classify_id=None):
    if classify_id is None:
        return Comic.query.all()
    else:
        return Comic.query.filter_by(classify_id=classify_id).all()


# 根据id获取图片
def get_comic(comic_id):
    return Comic.query.get(comic_id)


# 根据id获取章节列表
def get_chapters(comic_id=None):
    if comic_id is None:
        return Chapter.query.order_by(Chapter.chapter_number.desc()).all()
    return Chapter.query.filter_by(comic_id=comic_id).order_by(Chapter.chapter_number.desc()).all()


# 根据章节id获取指定的章节
def get_chapter(chapter_id):
    return Chapter.query.get(chapter_id)


# 获取下一章节的内容
def get_next_chapter(comic_id, chapter_number):
    chapter = Chapter.query.filter(
        and_(Chapter.comic_id == comic_id, Chapter.chapter_number > chapter_number)).order_by(
        Chapter.chapter_number.asc()).first()
    return chapter


# 获取前一章节的内容
def get_prev_chapter(comic_id, chapter_number):
    chapter = Chapter.query.filter(
        and_(Chapter.comic_id == comic_id, Chapter.chapter_number < chapter_number)).order_by(
        Chapter.chapter_number.desc()).first()
    return chapter


# 获取最后一章节
def get_latest_chapters(cnt=10):
    return Chapter.query.order_by(Chapter.refresh_time.desc()).limit(cnt).all()
