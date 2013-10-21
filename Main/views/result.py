import re
from ..util import session
from ..models import *
import flask
import flask_login
import flask.views


class ResultView(flask.views.MethodView):
    def get(self, result_id):
        if result_id is not None and session.query(WorkoutResult).get(result_id) is not None:
            result = session.query(WorkoutResult).get(result_id)
            if result is not None:
                return flask.render_template('result.html', user=flask_login.current_user, result=result)
        return flask.render_template('404.html'), 404


class ResultMod(flask.views.MethodView):
    def get(self, result_id):
        workout = session.query(Workout).get(int(flask.request.args['wid']))
        if workout is not None:
            return flask.render_template('result_mod.html', user=flask_login.current_user, workout=workout)
        return flask.render_template('404.html'), 404

    def post(self, result_id):
        workout = session.query(Workout).get(int(flask.request.form['workout_id']))
        if workout is None:
            return flask.render_template('404.html'), 404
        if ResultMod.validate_result_data() != 0:
            return flask.redirect(flask.url_for('result_mod', wid=workout.id))

        for part in workout.parts:
            if flask.request.form.get('result_'+part.order) == "":
                flask.flash("All parts require results!", "error")
                return flask.redirect(flask.url_for('result_mod', wid=workout.id))
            if part.uom.lower() == "rounds":
                if not flask.request.form.get('result_' + part.order).isdigit():
                    flask.flash("Round result must be a number!", "error")
                    return flask.redirect(flask.url_for('result_mod', wid=workout.id))
            elif part.uom.lower() == "pounds":
                if not flask.request.form.get('result_' + part.order).isdigit():
                    flask.flash("Pound result must be a number!", "error")
                    return flask.redirect(flask.url_for('result_mod', wid=workout.id))
            elif part.uom.lower() == "time":
                regex = re.compile('\d{2}:\d{2}(:\d{2})?')
                if regex.match(flask.request.form.get('result_' + part.order)) is None:
                    flask.flash("Time result must be in the following format: mm:ss or hh:mm:ss!", "error")
                    return flask.redirect(flask.url_for('result_mod', wid=workout.id))

        result = WorkoutResult()
        result.user = flask_login.current_user
        result.workout_id = workout.id

        for part in workout.parts:
            result_data = flask.request.form['result_'+part.order]
            result_details = flask.request.form['detail_'+part.order]
            part_result = WorkoutPartResult(result_data)
            part_result.part = part
            part_result.details = result_details
            result.parts.append(part_result)

        session.add(result)
        session.commit()
        return flask.redirect(flask.url_for('known_result', result_id=result.id))

    @staticmethod
    def validate_result_data():
        error = 0
        if flask.request.form['workout_id'] == "":
            flask.flash("Unknown error!", "error")
            error += 1
        return error