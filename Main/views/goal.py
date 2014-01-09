from ..models import *
from ..forms import *
from ..util import db
from flask.ext.login import current_user, login_required
from flask import render_template, request, url_for
import flask.views
from flask.ext.login import login_required
import flask_login
import datetime

# All Goals
class Goals(flask.views.MethodView):
    @login_required
    def get(self):
        goals = Goal.query.all()
        pass

    @login_required
    def post(self):
        return GoalCRUD.create_goal()


## Goal CREATE View
class GoalCreate(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('goal_create.html')


## Goal EDIT View
class GoalEdit(flask.views.MethodView):
    @login_required
    def get(self, goal_id):
        if goal_id is not None:
            goal = Goal.query.get(goal_id)
            return flask.render_template('goal_edit.html', goal=goal)
        else:
            return flask.render_template('404.html'), 404


## Goal Part EDIT View
class GoalPartEdit(flask.views.MethodView):
    @login_required
    def get(self, goal_id):
        goal = Goal.query.get(goal_id)
        today = datetime.date.today().strftime("%Y-%m-%d")
        return flask.render_template('update_goal.html', goal=goal, user=flask_login.current_user, today=today)

## Goal CRUD
class GoalCRUD(flask.views.MethodView):
    @login_required
    def get(self, goal_id):
        if goal_id is None:
            viewed_user = User.query.get(flask.request.args['user_id'])
            return flask.render_template('goals_view.html', user=flask_login.current_user, viewed_user=viewed_user)
        else:
            goal = Goal.query.get(goal_id)
            return flask.render_template('goal_view.html', user=flask_login.current_user, goal=goal)

    @login_required
    def post(self, goal_id):
        method = flask.request.form.get('_method', '')
        if method == "PUT":
            return GoalCRUD.edit_goal(goal_id)
        elif method == "UPDATE":
            return GoalCRUD.create_goal_update(goal_id)
        else:
            return flask.render_template('404.html'), 404

    @staticmethod
    def create_goal_update(goal_id):
        if GoalCRUD.validate_goal_update() != 0:
            return flask.redirect(flask.url_for('goal_part', goal_id=goal_id))
        else:
            goal = Goal.query.get(goal_id)
            update = GoalPart()
            update.goal = goal
            update.description = flask.request.form['update']
            update.date = datetime.datetime.strptime(flask.request.form['date'], '%Y-%m-%d').date()
            db.session.add(update)
            db.session.commit()
            flask.flash("Successfully updated goal!", "success")
            return flask.redirect(flask.url_for('goal', goal_id=goal_id))

    @staticmethod
    def edit_goal(goal_id):
        if GoalCRUD.validate_goal_create() != 0:
            return flask.redirect(flask.url_for('goal_edit', goal_id=goal_id))
        else:
            goal = Goal.query.get(goal_id)
            goal.title = flask.request.form['title']
            if flask.request.form.get('active') == 'on':
                goal.active = True
            else:
                goal.active = False
            if flask.request.form.get('complete') == 'on':
                goal.complete = True
            else:
                goal.complete = False

            db.session.commit()
            flask.flash("Successfully updated goal!", "success")
            return flask.redirect(flask.url_for('goal', goal_id=goal_id))

    @staticmethod
    def delete_goal(goal_id):
        pass

    @staticmethod
    def create_goal():
        if GoalCRUD.validate_goal_create() != 0:
            return flask.redirect(flask.url_for('goal_create'))
        else:
            goal = Goal()
            goal.title = flask.request.form['title']
            if flask.request.form.get('active') == 'on':
                goal.active = True
            goal.user = flask_login.current_user

            db.session.add(goal)
            db.session.commit()
            flask.flash("Successfully created goal!", "success")
            return flask.redirect(flask.url_for('goal', goal_id=goal.id))

    @staticmethod
    def validate_goal_create():
        error = 0
        if flask.request.form['title'] == "":
            flask.flash("Title is required!", "error")
            error += 1
        return error

    @staticmethod
    def validate_goal_update():
        error = 0
        if flask.request.form['update'] == "":
            flask.flash("Update is required!", "error")
            error += 1
        if flask.request.form['date'] == "":
            flask.flash("Date is required!", "error")
            error += 1
        return error