import datetime
from ..util import session
from ..models import *
import flask
import flask_login
import flask.views


class SearchView(flask.views.MethodView):
    def get(self):
        return flask.render_template('search.html', user=flask_login.current_user)
    def post(self):
        original_radio = flask.request.form.get('optionsRadios')
        original_from_date = flask.request.form.get('from_date')
        original_to_date = flask.request.form.get('to_date')
        original_tags = flask.request.form.getlist('tags[]')

        from_date = original_from_date
        if from_date == "":
            from_date = "1900-01-01"

        to_date = original_to_date
        if to_date == "":
            to_date = "9999-12-31"

        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        tags = SearchView.fixTags(original_tags)

        if from_date > to_date:
            flask.flash("From Date must come before To Date!", "error")
            results = None
        else:
            if original_radio == "user":
                results = SearchView.getUserResults(from_date, to_date, tags)
            elif original_radio == "gym":
                results = SearchView.getGymResults(from_date, to_date)
            else:
                results = SearchView.getAllResults(from_date, to_date)

        print "*********************** searching from " + str(from_date) + " to " + str(to_date)
        print "*********************** got: " + str(results)

        return flask.render_template('search.html',
                                     results=results,
                                     tags=tags,
                                     radio=original_radio,
                                     from_date=original_from_date,
                                     to_date=original_to_date,
                                     user=flask_login.current_user)

    @staticmethod
    def fixTags(tags):
        final_tags = ""
        for tag in tags[0].split(','):
            final_tags += str(tag.strip()) + ","
        return str(final_tags)[:-1]

    @staticmethod
    def getUserResults(from_date, to_date, tags):
        results = session.query(WorkoutResult).filter(WorkoutResult.user_id == flask_login.current_user.id).all()
        final_results = []
        for result in results:
            if from_date <= result.workout.post_date <= to_date:
                if not tags or tags == "":
                    final_results.append(result)
                else:
                    for part in result.workout.parts:
                        for tag in part.tags:
                            if any(tag.name in test_tag for test_tag in tags.split(',')):
                                final_results.append(result)
        return final_results

    @staticmethod
    def getGymResults(from_date, to_date):
        results = session.query(WorkoutResult).all()
        final_results = []
        for result in results:
            if from_date <= result.workout.post_date <= to_date:
                if result.workout.gym_id == flask_login.current_user.member_of_gym.id:
                    final_results.append(result)
        return final_results

    @staticmethod
    def getAllResults(from_date, to_date):
        results = session.query(WorkoutResult).all()
        final_results = []
        for result in results:
            if from_date <= result.workout.post_date <= to_date:
                final_results.append(result)
        return final_results