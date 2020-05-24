from flask import Flask
from route import register_route
from config.config import init_logging_config

app = Flask(__name__)

# UTF-8 서포트
app.config['JSON_AS_ASCII'] = False
register_route(app)
init_logging_config()

if __name__ == '__main__':
    app.run()
