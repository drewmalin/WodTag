from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from Main import app

lm = LoginManager()
lm.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WodTag.sqlite'
db = SQLAlchemy(app)