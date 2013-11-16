import re
from ..util import db
from ..models import *
from flask.ext.login import login_required
import flask
import flask_login
import flask.views


## All Results
class Results(flask.views.MethodView):
    @login_required
    def get(self):
        results = WorkoutResult.query.all()
        pass

    @login_required
    def post(self):
        return ResultCRUD.create_result()


## Result CREATE View
class ResultCreate(flask.views.MethodView):
    @login_required
    def get(self, workout_id):
        if workout_id is not None:
            workout = Workout.query.get(workout_id)
            return flask.render_template('result_create.html', workout=workout)
        else:
            return flask.render_template('404.html'), 404


## Result EDIT View
class ResultEdit(flask.views.MethodView):
    @login_required
    def get(self, result_id):
        if result_id is not None:
            result = WorkoutResult.query.get(result_id)
            return flask.render_template('result_edit.html', result=result)
        else:
            return flask.render_template('404.html'), 404


## Result CRUD
class ResultCRUD(flask.views.MethodView):
    @login_required
    def get(self, result_id):
        if result_id is not None and WorkoutResult.query.get(result_id) is not None:
            result = WorkoutResult.query.get(result_id)
            if result is not None:
                return flask.render_template('result.html', user=flask_login.current_user, result=result)
        return flask.render_template('404.html'), 404

    @login_required
    def post(self, result_id):
        method = flask.request.form.get('_method', '')
        if method == "PUT":
            return ResultCRUD.edit_result(result_id)
        elif method == "DELETE":
            return ResultCRUD.delete_result(result_id)
        else:
            return flask.render_template('404.html'), 404

    @staticmethod
    def edit_result(result_id):
        workout_id = flask.request.form['workout_id']
        if ResultCRUD.validate_result_create(workout_id) != 0:
            return flask.redirect(flask.url_for('result_create', workout_id=workout_id))
        else:
            result = WorkoutResult.query.get(result_id)
            for part in result.parts:
                part.result = flask.request.form['result_'+part.order]
                part.details = flask.request.form['detail_'+part.order]
            db.session.commit()
            flask.flash("Successfully updated workout result!", "success")
            return flask.redirect(flask.url_for('result', result_id=result_id))

    @staticmethod
    def delete_result(result_id):
        pass

    @staticmethod
    def create_result():
        workout_id = flask.request.form['workout_id']
        if ResultCRUD.validate_result_create(workout_id) != 0:
            return flask.redirect(flask.url_for('result_create', workout_id=workout_id))
        else:
            result = WorkoutResult()
            result.user = flask_login.current_user
            result.workout_id = workout_id
            for part in Workout.query.get(workout_id).parts:
                result_data = flask.request.form['result_'+part.order]
                result_details = flask.request.form['detail_'+part.order]
                part_result = WorkoutPartResult(result_data)
                part_result.order = part.order
                part_result.part = part
                part_result.details = result_details
                result.parts.append(part_result)
            db.session.add(result)
            db.session.commit()
            flask.flash("Successfully recorded workout!", "success")
            return flask.redirect(flask.url_for('result', result_id=result.id))


    @staticmethod
    def validate_result_create(workout_id):
        error = 0
        if workout_id == "":
            flask.flash("Unable to create result for null workout!", "error")
            error += 1
        workout = Workout.query.get(int(workout_id))
        for part in workout.parts:
            if flask.request.form.get('result_'+part.order) == "":
                flask.flash("All parts require results!", "error")
                error += 1
            if part.uom.lower() == "rounds":
                if not flask.request.form.get('result_' + part.order).isdigit():
                    flask.flash("Round result must be a number!", "error")
                    error += 1
            elif part.uom.lower() == "pounds":
                if not flask.request.form.get('result_' + part.order).isdigit():
                    flask.flash("Pound result must be a number!", "error")
                    error += 1
            elif part.uom.lower() == "time":
                regex = re.compile('(\d{1,2}:)?\d{1,2}:\d{2}')
                if regex.match(flask.request.form.get('result_' + part.order)) is None:
                    flask.flash("Time result must be in the following format: mm:ss or hh:mm:ss!", "error")
                    error += 1
        return error