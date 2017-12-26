# coding=utf-8

from apscheduler.triggers.interval import IntervalTrigger
from flask_apscheduler import APScheduler
from photohub.tasks import task

scheduler = APScheduler()


# 初始化调度器
def init_scheduler(app):
    scheduler.init_app(app)

    # 刷新图片集
    def __refresh_comics():
        with app.app_context():
            task.refresh_comics()
            task.refresh_comic_images()

    # 刷新章节
    def __refresh_chapters():
        with app.app_context():
            task.refresh_chapters()

    # 开始执行任务
    scheduler.add_job('refresh_comics', __refresh_comics, max_instances=1,
                      trigger=IntervalTrigger(weeks=1))

    scheduler.add_job('refresh_chapters', __refresh_chapters, max_instances=1,
                      trigger=IntervalTrigger(hours=1))
    scheduler.start()
