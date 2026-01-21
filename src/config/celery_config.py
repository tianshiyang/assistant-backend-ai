import os
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


def init_celery_config(app: Flask) -> Celery:
    # Celery 配置
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = os.getenv("REDIS_PORT", "6379")
    redis_password = os.getenv("REDIS_PASSWORD", "")

    # 构建 Redis URL
    broker_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
    result_backend_url = f"redis://:{redis_password}@{redis_host}:{redis_port}/1"

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
        ),
    )

    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.autodiscover_tasks(
        ["src.task"],
        force=True
    )
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app