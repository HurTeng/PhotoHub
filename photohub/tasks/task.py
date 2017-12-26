# coding=utf-8

import datetime
import json

import requests
from flask import current_app
from sqlalchemy import and_

import photohub.data as data
from photohub.extensions.flasksqlalchemy import db
from photohub.models.chapter import Chapter
from photohub.models.comic import Comic

COMICS_URL = "http://www.photohub.net/ComicBooks/GetAllBook"
CHAPTER_URL = "http://www.photohub.net/ComicBooks/GetChapterList"


# 加载相关页面的图片
def load_comics(page):
    response = requests.get(COMICS_URL, params={"PageIndex": page})
    return response.json()['Return']['List']


# 加载章节
def load_chapters(page, comic_id):
    response = requests.get(CHAPTER_URL, params={"PageIndex": page, "id": comic_id})
    return response.json()['Return']['List']


# 解析数据
def parse_date(time_str):
    """
    :param time_str: like "/Date(1453196817000)/"
    :return: datetime
    """
    timestamp = int(time_str[6:-2])
    return datetime.datetime.fromtimestamp(timestamp / 1e3)


# 刷新图片集
def refresh_comics():
    # 加载漫画
    page = 0
    comics = load_comics(page)
    # 打印log
    current_app.logger.info('get {} comics of page {}'.format(len(comics), page))
    result = []
    while len(comics) > 0:
        for comic in comics:
            try:
                # 根据id查看动漫是否存在
                if Comic.query.get(comic['Id']):
                    current_app.logger.info('comic {} already existed'.format(comic['Id']))
                    continue

                # 如果不存在,添加到数据库中
                new_comic = Comic()
                new_comic.id = comic['Id']
                new_comic.title = comic['Title']
                new_comic.description = comic['Explain']
                new_comic.refresh_time = parse_date(comic['RefreshTime'])
                new_comic.author = comic['Author']
                new_comic.classify_id = comic['ClassifyId']
                new_comic.front_cover = comic['FrontCover']
                db.session.add(new_comic)
                db.session.commit()
                result.append(comic['Id'])
            except Exception as e:
                current_app.logger.error('exception occur when save comic {} :{}'.format(comic['Id'], e))
        # 继续获取下一页数据
        page += 1
        comics = load_comics(page)
    return result


# 刷新指定章节
def refresh_chapter(comic_id):
    # 加载章节
    page = 0
    chapters = load_chapters(page, comic_id)
    saved_chapter_num = 0
    while len(chapters) > 0:
        for chapter in chapters:
            try:
                # 根据id查看章节是否存在
                database_chapter = Chapter.query.get(chapter['Id'])
                if database_chapter:
                    same_chapter_number_chapters = Chapter.query.filter(
                        and_(Chapter.comic_id == database_chapter.comic_id,
                             Chapter.chapter_number == database_chapter.chapter_number)).all()
                    for same_chapter_number_chapter in same_chapter_number_chapters:
                        if same_chapter_number_chapter.id != database_chapter.id:
                            # delete duplicate chapters
                            db.session.delete(same_chapter_number_chapter)
                    continue

                # 如果不存在,添加到数据库中
                new_chapter = Chapter()
                new_chapter.id = chapter['Id']
                new_chapter.title = chapter['Title']
                new_chapter.comic_id = comic_id
                new_chapter.chapter_number = chapter['ChapterNo']
                new_chapter.front_cover = chapter['FrontCover']
                new_chapter.refresh_time = parse_date(chapter['RefreshTime'])
                db.session.add(new_chapter)
                saved_chapter_num += 1
            except Exception as e:
                current_app.logger.warning(e)
        # 继续获取下一章节的数据
        page += 1
        chapters = load_chapters(page, comic_id)
    db.session.commit()
    current_app.logger.info('saved {} chapters of comic {}'.format(saved_chapter_num, comic_id))
    return comic_id, saved_chapter_num


# 刷新图片集
def refresh_comic_images():
    # 获取动漫列表
    comics = data.get_comics()
    result = dict()
    for comic in comics:
        # 获取动漫封面
        front_cover = comic.front_cover
        if 'photohub' not in front_cover:
            current_app.logger.info('comic {} already refreshed'.format(comic.id))
            continue
        # 获取图片集列表
        image = requests.get(front_cover).content
        files = {'smfile': image}
        # 请求数据
        response = json.loads(requests.post('https://sm.ms/api/upload', files=files).text)
        if response.get('code') == 'success':
            # 请求成功的话,获取图片链接
            url = response.get('data')['url']
            comic.front_cover = url
            # 保存到数据库中
            db.session.commit()
            result[comic.id] = url
            current_app.logger.info('refresh comic {} cover succeed, url :{}'.format(
                comic.id, url))
        else:
            current_app.logger.info('failed comic {}'.format(comic.id))
    return result


# 刷新章节
def refresh_chapters():
    # 获取动漫列表
    comics = data.get_comics()
    result = {}
    # 返回动漫数据
    for comic in comics:
        comic_id, saved_chapter_num = refresh_chapter(comic.id)
        result[comic_id] = saved_chapter_num
    return result
