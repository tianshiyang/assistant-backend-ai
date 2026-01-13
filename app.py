from logging import exception

from flask_cors import CORS
from flask import Flask
import os
import dotenv

from pkg.exception.exception import CustomException
from pkg.response import json, Response, HttpCode
from router import account_blueprint

app = Flask(__name__)

dotenv.load_dotenv()

# 注册路由
app.register_blueprint(
    # 账号模块
    account_blueprint,
)

# 配置 SECRET_KEY（Flask-WTF 需要）
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 禁用 CSRF（API 项目通常不需要 CSRF 保护，使用 token 认证）
app.config['WTF_CSRF_ENABLED'] = False

def _register_error_handler(error: Exception):
    if isinstance(error, CustomException):
        return json(Response(
            code=error.code,
            message=error.message,
            data=error.data,
        ))
    return json(Response(
        code=HttpCode.ERROR,
        message=str(error),
        data={},
    ))


# 自定义异常
app.register_error_handler(Exception, _register_error_handler)

# 跨域配置
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "supports_credentials": True,
        # "methods": ["GET", "POST"],
        # "allow_headers": ["Content-Type"],
    }
})


if __name__ == '__main__':
    app.run(debug=True)
