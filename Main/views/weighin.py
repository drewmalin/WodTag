from ..models import *
from ..forms import *
from ..util import db
from flask.ext.login import current_user, login_required
from flask import render_template, request, url_for
import flask.views
from flask.ext.login import login_required
import flask_login
import datetime

"""
class WeighIns(flask.views.View):
    @login_required
    def dispatch_request(self):
        form = WeighInForm(request.form)
        weighins = WeighIn.query.filter_by(user_id=current_user.id)
        if request.method == 'POST' and form.validate_on_submit():
            weigh_in = WeighIn(form.weight.data, current_user.id, form.date.data)
            db.session.add(weigh_in)
            db.session.commit()
            return render_template('weigh_in.html', form=form, weighins=weighins)

        return render_template('weigh_in.html', form=form, weighins=weighins)
"""

# All Weighins
class WeighIns(flask.views.MethodView):
    @login_required
    def get(self):
        weighins = WeighIn.query.all()
        pass

    @login_required
    def post(self):
        return WeighInCRUD.create_weighin()


## WeighIn CREATE View
class WeighInCreate(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('weighin_create.html')


## WeighIn EDIT View
class WeighInEdit(flask.views.MethodView):
    @login_required
    def get(self, weighin_id):
        if weighin_id is not None:
            weighin = WeighIn.query.get(weighin_id)
            return flask.render_template('weighin_edit.html', weighin=weighin)
        else:
            return flask.render_template('404.html'), 404

## WeighIn CRUD
class WeighInCRUD(flask.views.MethodView):
    @login_required
    def get(self, weighin_id):
        return flask.render_template('weighin.html', user=flask_login.current_user)

    @login_required
    def post(self, weighin_id):
        method = flask.request.form.get('_method', '')
        if method == "PUT":
            return WeighInCRUD.edit_weighin(weighin_id)
        elif method == "DELETE":
            return WeighInCRUD.delete_weighin(weighin_id)
        else:
            return flask.render_template('404.html'), 404

    @staticmethod
    def edit_weighin(weighin_id):
        if WeighInCRUD.validate_weighin_create() != 0:
            return flask.redirect(flask.url_for('weighin_edit', weighin_id=weighin_id))
        else:
            weighin = WeighIn.query.get(weighin_id)
            weighin.weight = flask.request.form['weight']
            weighin.date = datetime.datetime.strptime(flask.request.form['date'], '%Y-%m-%d').date()
            weighin.body_fat = flask.request.form.get('bodyfat')
            weighin.muscle_mass = flask.request.form.get('musclemass')
            db.session.commit()
            flask.flash("Successfully updated weigh-in!", "success")
            return flask.redirect(flask.url_for('weighin_view'))

    @staticmethod
    def delete_weighin(weighin_id):
        pass

    @staticmethod
    def create_weighin():
        if WeighInCRUD.validate_weighin_create() != 0:
            return flask.redirect(flask.url_for('weighin_create'))
        else:
            weighin = WeighIn(flask.request.form['weight'])
            weighin.date = datetime.datetime.strptime(flask.request.form['date'], '%Y-%m-%d').date()
            weighin.body_fat = flask.request.form.get('bodyfat')
            weighin.muscle_mass = flask.request.form.get('musclemass')
            weighin.user = flask_login.current_user
            db.session.add(weighin)
            db.session.commit()
            flask.flash("Successfully recorded weigh-in!", "success")
            return flask.redirect(flask.url_for('weighin_view'))

    @staticmethod
    def validate_weighin_create():
        error = 0
        if flask.request.form['weight'] == "":
            flask.flash("Weight is required!", "error")
            error += 1
        if flask.request.form['date'] == "":
            flask.flash("Date is required!", "error")
            error += 1
        return error