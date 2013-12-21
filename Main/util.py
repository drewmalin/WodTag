from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.sendmail import Mail
from Main import app

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
lm.login_message_category = 'error'
lm.refresh_view = 'index'
lm.needs_refresh_message = 'You have been logged out due to inactivity.'
lm.needs_refresh_message_category = 'error'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WodTag.sqlite'

app.config.update(dict(
    MAIL_FAIL_SILENTLY=False,
    MAIL_SUPPRESS_SEND=False,
    TESTING=False
))

db = SQLAlchemy(app)
mail = Mail(app)