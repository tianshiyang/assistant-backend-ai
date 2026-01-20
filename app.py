from flask import Flask
import dotenv

from src.config import (
    init_flask_router, 
    init_flask_error, 
    init_flask_app_config, 
    init_db_config, 
    init_flask_jwt_config,
    celery_config
)

# 先加载环境变量
dotenv.load_dotenv()

app = Flask(__name__)

# 初始化应用配置
init_flask_app_config(app)

# 初始化数据库
init_db_config(app)

init_flask_jwt_config(app)

# 初始化 Celery（必须在路由初始化之前）
celery = celery_config(app)

# 初始化路由
init_flask_router(app)

# 初始化错误处理
init_flask_error(app)


if __name__ == '__main__':
    app.run(debug=True)
