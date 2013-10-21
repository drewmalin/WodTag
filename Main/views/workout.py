import datetime
from ..util import session
from ..models import *
import flask
import flask_login
import flask.views


class WorkoutTemplateView(flask.views.MethodView):
    def get(self, workout_template_id):
        if workout_template_id is not None and session.query(Workout).get(workout_template_id) is not None:
            workout = session.query(Workout).get(workout_template_id)
            if workout is not None:
                return flask.render_template('workout_template.html', workout=workout, user=flask_login.current_user)
        return flask.render_template('404.html'), 404


class WorkoutTemplateMod(flask.views.MethodView):
    def get(self):
        return flask.render_template('workout_template_mod.html')

    def post(self):
        if WorkoutTemplateMod.validate_user_data() != 0:
            return flask.redirect(flask.url_for('workout_template_mod'))

        parts = WorkoutTemplateMod.collect_parts()

        workout = Workout(flask.request.form['workout_name'])
        workout.post_date = datetime.datetime.strptime(flask.request.form['workout_date'], '%Y-%m-%d').date()
        workout.gym = flask_login.current_user.owns_gym

        for idx in parts:
            part = WorkoutPart(parts[idx]['name'])
            part.order = idx
            part.uom = parts[idx]['uom']
            for tag_name in parts[idx]['tags'].split(','):
                if tag_name != "":
                    tag = session.query(Tag).filter_by(name=tag_name).first()
                    if tag is None:
                        tag = Tag(tag_name)
                    part.tags.append(tag)
            workout.parts.append(part)

        session.add(workout)
        session.commit()
        return flask.redirect(flask.url_for('workout_template', workout_template_id=workout.id))

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

class WorkoutTemplateResults(flask.views.MethodView):
    def get(self, workout_template_id):
        if workout_template_id is not None and session.query(Workout).get(workout_template_id) is not None:
            workout = session.query(Workout).get(workout_template_id)
            if workout is not None:
                return flask.render_template('workout_template_results.html', workout=workout, user=flask_login.current_user)
        return flask.render_template('404.html'), 404