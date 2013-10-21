from ..util import session
from ..models import *
import flask
import flask.views
import flask_login
import hashlib


class Index(flask.views.MethodView):
    def get(self):
        if not flask_login.current_user.is_anonymous():
            return flask.redirect(flask.url_for('known_user', user_id=flask_login.current_user.id))
        else:
            flask_login.logout_user()
            return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask_login.logout_user()
            return flask.redirect(flask.url_for('index'))
        if flask.request.form['username'] == "":
            flask.flash("Username is required!", "error")
            return flask.redirect(flask.url_for('index'))
        elif flask.request.form['password'] == "":
            flask.flash("Password is required!", "error")
            return flask.redirect(flask.url_for('index'))

        user = None
        user_name = flask.request.form['username'].strip()
        user_pass = flask.request.form['password']
        for test_user in session.query(User).filter_by(username=user_name):
            if test_user.password == hashlib.sha1(user_pass + test_user.salt).hexdigest():
                user = test_user
                break

        if not user:
            flask.flash("Username or password is incorrect!", "error")
            return flask.redirect(flask.url_for('index'))
        else:
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('known_user', user_id=flask_login.current_user.id))