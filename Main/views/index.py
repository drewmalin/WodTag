from ..models import *
from flask.ext.login import login_required
import flask
import flask.views
import flask_login
import hashlib


class Index(flask.views.MethodView):
    def get(self):
        if not flask_login.current_user.is_anonymous():
            return flask.redirect(flask.url_for('user', user_id=flask_login.current_user.id))
        else:
            flask_login.logout_user()
            return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask_login.logout_user()
            return flask.redirect(flask.url_for('index'))
        else:
            return Index.login_user()

    @staticmethod
    def login_user():
        if Index.validate_login_data() != 0:
            return flask.redirect(flask.url_for('index'))
        else:
            return Index.process_login()


    @staticmethod
    def validate_login_data():
        error = 0
        if flask.request.form['username'] == "":
            flask.flash("Username is required!", "error")
            error += 1
        elif flask.request.form['password'] == "":
            flask.flash("Password is required!", "error")
            error += 1
        return error

    @staticmethod
    def process_login():
        user = None
        user_name = flask.request.form['username'].strip()
        user_pass = flask.request.form['password']
        for test_user in User.query.filter_by(username=user_name).all():
            if test_user.password == hashlib.sha1(user_pass + test_user.salt).hexdigest():
                user = test_user
                break

        if not user:
            flask.flash("Username or password is incorrect!", "error")
            return flask.redirect(flask.url_for('index'))
        else:
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('user', user_id=flask_login.current_user.id))