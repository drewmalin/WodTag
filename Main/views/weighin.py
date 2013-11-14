from ..models import *
from ..forms import *
from ..util import db
from flask.ext.login import current_user, login_required
from flask import render_template, request, url_for
import flask.views


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

