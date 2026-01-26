import os
from urllib.parse import quote_plus

from celery import Celery, Task
from celery.signals import setup_logging
from flask import Flask

from .log_config import init_log_config


@setup_logging.connect
def config_celery_logging(**kwargs):
    """
    Celery worker 启动时自动配置日志
    这个函数会在 Celery worker 启动时被调用
    """
    init_log_config()


def _build_redis_url(db: int) -> str:
    """从 .env 中的 Redis 连接信息 + 指定 DB 号拼出 Celery 用的 Redis URL。"""
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", "6379")
    username = os.getenv("REDIS_USERNAME") or ""
    password = os.getenv("REDIS_PASSWORD") or ""
    # user_part = f"{quote_plus(username)}:{quote_plus(password)}"
    return f"redis://:{password}@{host}:{port}/{db}"


def init_celery_config(app: Flask) -> Celery:
    broker_db = int(os.getenv("CELERY_BROKER_DB", "0"))
    backend_db = int(os.getenv("CELERY_RESULT_BACKEND_DB", "1"))
    broker_url = _build_redis_url(broker_db)
    result_backend_url = _build_redis_url(backend_db)

    app.config.from_mapping(
        CELERY=dict(
            broker_url=broker_url,
            result_backend=result_backend_url,
            task_ignore_result=True,
            task_serializer="json",
            result_serializer="json",
            accept_content=["json"],
            timezone="UTC",
            enable_utc=True,
            # 定时任务配置（Celery Beat）
            beat_schedule={
                'cleanup-old-logs': {
                    'task': 'src.task.cleanup_log_task.cleanup_old_logs_task',
                    'schedule': 86400.0,  # 每24小时执行一次（秒）
                    'options': {'expires': 3600}  # 任务过期时间1小时
                },
            },
        ),
    )

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()  # 设置为默认实例，这样 @shared_task 才能正确绑定
    celery_app.autodiscover_tasks(
        ["src.task"],
        force=True
    )
    app.extensions["celery"] = celery_app
    return celery_app