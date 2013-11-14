import datetime
from ..util import db
from ..models import *
from flask.ext.login import login_required
import flask
import flask_login
import flask.views


## All Workouts
class Workouts(flask.views.MethodView):
    @login_required
    def get(self):
        workouts = db.session.query(Workout).all()
        pass

    @login_required
    def post(self):
        return WorkoutCRUD.create_workout()


## Workout CREATE View
class WorkoutCreate(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('workout_create.html')


## Workout EDIT View
class WorkoutEdit(flask.views.MethodView):
    @login_required
    def get(selfself, workout_id):
        if workout_id is not None:
            workout = Workout.query.get(workout_id)
            return flask.render_template('workout_edit.html', workout=workout)
        else:
            return flask.render_template('404.html'), 404


## Workout CRUD
class WorkoutCRUD(flask.views.MethodView):
    @login_required
    def get(self, workout_id):
        if workout_id is not None and Workout.query.get(workout_id) is not None:
            workout = Workout.query.get(workout_id)
            if workout is not None:
                return flask.render_template('workout.html', workout=workout, user=flask_login.current_user)
        return flask.render_template('404.html'), 404

    @login_required
    def post(self, workout_id):
        method = flask.request.form.get('_method', '')
        if method == "PUT":
            pass
        elif method == "DELETE":
            pass
        else:
            return flask.render_template('404.html'), 404

    @staticmethod
    def edit_workout(workout_id):
        pass

    @staticmethod
    def delete_workout(workout_id):
        pass

    @staticmethod
    def create_workout():
        if WorkoutCRUD.validate_user_data() != 0:
            return flask.redirect(flask.url_for('workout_create'))
        else:
            parts = WorkoutCRUD.collect_parts()

            workout = Workout(flask.request.form['workout_name'])
            workout.post_date = datetime.datetime.strptime(flask.request.form['workout_date'], '%Y-%m-%d').date()
            workout.gym = flask_login.current_user.owns_gym

            for idx in parts:
                part = WorkoutPart(parts[idx]['name'])
                part.order = idx
                part.uom = parts[idx]['uom']
                for tag_name in parts[idx]['tags'].split(','):
                    if tag_name != "":
                        tag = Tag.query.filter_by(name=tag_name).first()
                        if tag is None:
                            tag = Tag(tag_name)
                        part.tags.append(tag)
                workout.parts.append(part)

            db.session.add(workout)
            db.session.commit()
            return flask.redirect(flask.url_for('workout', workout_id=workout.id))

    @staticmethod
    def collect_parts():
        f = flask.request.form
        parts = {}
        for key in f.keys():
            if "[part]" in key:
                idx = key[key.find('[')+1:key.find(']')]
                part = {'name': flask.request.form[key], 'uom': flask.request.form[key.replace('[part]', '[uom]')]}
                if key.replace('[part]', '[tags]') in f.keys():
                    part['tags'] = str(f.getlist(key.replace('[part]', '[tags]'))).strip()[3:-2]
                parts[idx] = part
        return parts

    @staticmethod
    def validate_user_data():
        error = 0
        if flask.request.form['workout_name'] == "":
            flask.flash("Workout name is required!", "error")
            error += 1
        if flask.request.form['workout_date'] == "":
            flask.flash("Workout date is required!", "error")
            error += 1
        return error


class WorkoutResults(flask.views.MethodView):
    @login_required
    def get(self, workout_id):
        if workout_id is not None and Workout.query.get(workout_id) is not None:
            workout = Workout.query.get(workout_id)
            if workout is not None:
                return flask.render_template('workout_results.html', workout=workout, user=flask_login.current_user)
        return flask.render_template('404.html'), 404