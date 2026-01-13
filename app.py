from flask import Flask
import dotenv

from config import init_flask_router, init_flask_error, init_flask_app_config

app = Flask(__name__)

init_flask_router(app)
init_flask_error(app)
init_flask_app_config(app)

dotenv.load_dotenv()


if __name__ == '__main__':
    app.run(debug=True)
