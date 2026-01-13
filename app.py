from flask_cors import CORS
from flask import Flask
import os
import dotenv
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

# 跨域配置
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "supports_credentials": True,
        # "methods": ["GET", "POST"],
        # "allow_headers": ["Content-Type"],
    }
})


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
