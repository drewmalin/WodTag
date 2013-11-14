from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from Main import app

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
lm.login_message_category = 'error'
lm.refresh_view = 'index'
lm.needs_refresh_message = 'You have been logged out due to inactivity.'
lm.needs_refresh_message_category = 'error'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WodTag.sqlite'
db = SQLAlchemy(app)