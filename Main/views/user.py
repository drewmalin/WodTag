from ..util import session
from ..models import *
import flask
import flask_login
import flask.views


class UserView(flask.views.MethodView):
    def get(self, user_id):
        print user_id
        if user_id is not None and session.query(User).get(user_id) is not None:
            user = session.query(User).get(user_id)
            if user is not None:
                return flask.render_template('user.html', viewed_user=user, user=flask_login.current_user, uid=flask_login.current_user.id)
        return flask.render_template('404.html'), 404


class UserMod(flask.views.MethodView):
    def get(self, user_id):
        if user_id is not None:
            user = session.query(User).get(user_id).first()
        else:
            user = None
        return flask.render_template('user_mod.html', user=user)

    def post(self, user_id):
        if user_id is None:
            user = self.new_user()
            if user is None:
                return flask.redirect(flask.url_for('user_mod'))
            else:
                return flask.redirect(flask.url_for('index'))
        else:
            user = self.edit_user(user_id)
            if user is None:
                return flask.redirect(flask.url_for('user_mod', user_id=user_id))
            else:
                return flask.redirect(flask.url_for('index'))

    def new_user(self):
        if UserMod.validate_user_data() != 0:
            return None
        user = User(flask.request.form['username'], flask.request.form['password'])
        type = flask.request.form.get('user_type', '')
        if type == "owner":
            user.is_gym_owner = True
        session.add(user)
        session.commit()
        return user

    def edit_user(self, user_id):
        if UserMod.validate_user_data() != 0:
            return None

        user = session.query(User).get(user_id).first()
        # no edits for now
        return user

    @staticmethod
    def validate_user_data():
        error = 0
        if flask.request.form['username'] == "":
            flask.flash("Username is required!", "error")
            error += 1
        elif flask.request.form['password'] == "" or flask.request.form['password2'] == "":
            flask.flash("Password is required!", "error")
            error += 1
        elif flask.request.form['password'] != flask.request.form['password2']:
            flask.flash("Passwords must match!", "error")
            error += 1
        type = flask.request.form.get('user_type', '')
        if not type:
            flask.flash("Define membership type!", "error")
            error += 1
        return error