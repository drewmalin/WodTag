from ..util import session
from ..models import *
import flask
import flask_login
import flask.views


class GymView(flask.views.MethodView):
    def get(self, gym_id):
        if gym_id is not None and session.query(Gym).get(gym_id) is not None:
            gym = session.query(Gym).get(gym_id)
            user = flask_login.current_user
            results = {}
            for result in user.results:
                results[result.workout.id] = result.id
            owns = user.owns_gym is not None and user.owns_gym.id == gym.id
            member = user.member_of_gym is not None and user.member_of_gym.id == gym.id
            return flask.render_template('gym.html', gym=gym, user=user, user_is_owner=owns, user_is_member=member, user_posted_results=results)
        else:
            return flask.render_template('404.html'), 404

    def post(self, gym_id):
        gym = session.query(Gym).get(gym_id)
        if gym_id is not None and gym is not None:
            user = flask_login.current_user
            gym.members.append(user)
            session.commit()
            flask.flash("Successfully joined " + gym.name + "!", "success")
            return flask.redirect(flask.url_for('known_gym', gym_id=gym_id))
        else:
            return flask.render_template('404.html'), 404


class AllGymsView(flask.views.MethodView):
    def get(self):
        gyms = session.query(Gym)
        return flask.render_template('all_gyms.html', gyms=gyms, user=flask_login.current_user)


class AllGymMembersView(flask.views.MethodView):
    def get(self, gym_id):
        if gym_id is not None and session.query(Gym).get(gym_id) is not None:
            gym = session.query(Gym).get(gym_id)
            return flask.render_template('gym_members.html', gym=gym)
        else:
            return flask.render_template('404.html'), 404


class AllGymOwnersView(flask.views.MethodView):
    def get(self, gym_id):
        if gym_id is not None and session.query(Gym).get(gym_id) is not None:
            gym = session.query(Gym).get(gym_id)
            return flask.render_template('gym_owners.html', gym=gym)
        else:
            return flask.render_template('404.html'), 404


class GymMod(flask.views.MethodView):
    def get(self, gym_id):
        if gym_id is not None:
            gym = session.query(Gym).get(gym_id).first()
        else:
            gym = None
        return flask.render_template('gym_mod.html', gym=gym)

    def post(self, gym_id):
        if gym_id is None:
            gym = self.new_gym()
            if gym is None:
                return flask.redirect(flask.url_for('gym_mod'))
            else:
                return flask.redirect(flask.url_for('known_gym', gym_id=gym.id))
        else:
            gym = self.edit_gym(gym_id)
            if gym is None:
                return flask.redirect(flask.url_for('gym_mod', gym_id=gym_id))
            else:
                return flask.redirect(flask.url_for('known_gym', gym_id=gym_id))

    def new_gym(self):
        if self.validate_gym_data() != 0:
            return None
        gym = Gym(flask.request.form['gym_name'], flask.request.form['gym_description'])
        gym.owners.append(flask_login.current_user)
        session.add(gym)
        session.commit()
        return gym

    def edit_gym(self, gym_id):
        if self.validate_gym_data() != 0:
            return None

        gym = session.query(Gym).get(gym_id).first()
        # no edits for now
        return gym

    @staticmethod
    def validate_gym_data():
        error = 0
        if flask.request.form['gym_name'] == "":
            flask.flash("Gym name is required!", "error")
            error += 1
        return error