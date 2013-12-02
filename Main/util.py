from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from Main import app

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
lm.login_message_category = 'error'
lm.refresh_view = 'index'
lm.needs_refresh_message = 'You have been logged out due to inactivity.'
lm.needs_refresh_message_category = 'error'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///WodTag.sqlite'

"""
app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='drewmalin@gmail.com',
    MAIL_PASSWORD='',
))
"""

db = SQLAlchemy(app)
mail = Mail(app)