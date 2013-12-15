from ..util import db
from ..models import *
from flask.ext.login import login_required
import flask
import flask_login
import flask.views

WORKOUTS_PER_PAGE = 30

## All Gyms
class Gyms(flask.views.MethodView):
    @login_required
    def get(self):
        gyms = Gym.query.all()
        return flask.render_template('all_gyms.html', gyms=gyms, user=flask_login.current_user)

    @login_required
    def post(self):
        return Gyms.new_gym()

    @staticmethod
    def new_gym():
        if Gyms.validate_gym_data() != 0:
            flask.redirect(flask.url_for('gym_create'))
        gym = Gym(flask.request.form['gym_name'], flask.request.form['gym_description'])
        gym.owners.append(flask_login.current_user)
        gym.members.append(flask_login.current_user)
        db.session.add(gym)
        db.session.commit()
        return flask.redirect(flask.url_for('gym', gym_id=gym.id))

    @staticmethod
    def validate_gym_data():
        error = 0
        if flask.request.form['gym_name'] == "":
            flask.flash("Gym name is required!", "error")
            error += 1
        return error


## Gym CREATE View
class GymCreate(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('gym_create.html')


## Gym EDIT View
class GymEdit(flask.views.MethodView):
    @login_required
    def get(self, gym_id):
        if gym_id is not None:
            gym = Gym.query.get(gym_id)
            return flask.render_template('gym_edit.html', gym=gym)
        else:
            return flask.render_template('404.html'), 404


## Gym DELETE View
class GymDelete(flask.views.MethodView):
    def get(self, gym_id):
        pass


## Gym CRUD
class GymCRUD(flask.views.MethodView):
    @login_required
    def get(self, gym_id):
        if gym_id is not None and Gym.query.get(gym_id) is not None:
            gym = Gym.query.get(gym_id)
            user = flask_login.current_user
            results = {}
            page = flask.request.args.get('page')
            if page is None or int(page) <= 0:
                page = 1
            elif int(page) > int(len(gym.template_workouts) / WORKOUTS_PER_PAGE) + 1:
                page = int(len(gym.template_workouts) / WORKOUTS_PER_PAGE) + 1
            workouts = Workout.query.filter(Workout.gym_id==gym_id).order_by(Workout.post_date.desc()).\
                paginate(int(page), WORKOUTS_PER_PAGE, False)
            for result in user.results:
                results[result.workout.id] = result.id
            return flask.render_template('gym.html',
                                         gym=gym, user=user,
                                         user_is_owner=user.owns_gym is not None and user.owns_gym.id == gym.id,
                                         user_is_member=user.member_of_gym is not None and user.member_of_gym.id == gym.id,
                                         user_posted_results=results, workouts=workouts)
        else:
            return flask.render_template('404.html'), 404

    @login_required
    def post(self, gym_id):
        method = flask.request.form.get('_method', '')
        if method == "PUT":
            return GymCRUD.edit_gym(gym_id)
        elif method == "DELETE":
            return GymCRUD.delete_gym(gym_id)
        else:
            return GymCRUD.join_gym(gym_id)

    @staticmethod
    def edit_gym(gym_id):
        if GymCRUD.validate_gym_data() != 0:
            return flask.redirect(flask.url_for('gym_edit', gym_id=gym_id))
        else:
            gym = Gym.query.get(gym_id)
            gym.name = flask.request.form['gym_name']
            gym.description = flask.request.form['gym_description']
            db.session.add(gym)
            db.session.commit()
            return flask.redirect(flask.url_for('gym', gym_id=gym_id))

    @staticmethod
    def delete_gym(gym_id):
        pass

    @staticmethod
    def join_gym(gym_id):
        if gym_id is None:
            return flask.render_template('404.html'), 404
        gym = Gym.query.get(gym_id)
        if gym is None:
            return flask.render_template('404.html'), 404
        gym.members.append(flask_login.current_user)
        db.session.commit()
        flask.flash("Successfully joined " + gym.name + "!", "success")
        return flask.redirect(flask.url_for('gym', gym_id=gym_id))

    @staticmethod
    def validate_gym_data():
        error = 0
        if flask.request.form['gym_name'] == "":
            flask.flash("Gym name is required!", "error")
            error += 1
        return error


class AllGymMembersView(flask.views.MethodView):
    @login_required
    def get(self, gym_id):
        if gym_id is not None and Gym.query.get(gym_id) is not None:
            gym = Gym.query.get(gym_id)
            return flask.render_template('gym_members.html', gym=gym)
        else:
            return flask.render_template('404.html'), 404


class AllGymOwnersView(flask.views.MethodView):
    @login_required
    def get(self, gym_id):
        if gym_id is not None and Gym.query.get(gym_id) is not None:
            gym = Gym.query.get(gym_id)
            return flask.render_template('gym_owners.html', gym=gym)
        else:
            return flask.render_template('404.html'), 404