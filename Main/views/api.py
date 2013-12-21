from Main.decorators import crossdomain
from ..models import *
from flask.ext.login import login_required
import flask_login
import flask
import flask.views


class TagsAPI(flask.views.MethodView):
    @login_required
    @crossdomain(origin='*')
    def get(self, tag_id):
        if tag_id is None:
            tag_filter = flask.request.args.get('q')
            tag_list = []

            if not tag_filter:
                tags = Tag.query.limit(10).all()
            else:
                tags = Tag.query.filter(Tag.name.contains(tag_filter)).limit(10).all()

            for tag in tags:
                tag_list.append({'id': str(tag.id), 'text': tag.name})

            return flask.jsonify(tags=tag_list)
        else:
            pass


class WeighInAPI(flask.views.MethodView):
    @login_required
    @crossdomain(origin='*')
    def get(self):
        final_json = '{'
        weighins = WeighIn.query.filter_by(user_id=flask_login.current_user.id).order_by(WeighIn.date.asc())
        final_json += "\"dates\":["
        for weighin in weighins:
            final_json += "\"" + weighin.date.strftime('%m/%d/%Y') + "\","
        final_json = final_json[:-1] + "],"
        final_json += "\"data\": ["
        final_json += jsonify('Weight', 0, [w.date for w in weighins], [str(w.weight) for w in weighins], "#4572A7") + ","
        final_json += jsonify('Body Fat', 1, [w.date for w in weighins], [str(w.body_fat) for w in weighins], "#89A54E") + ","
        final_json += jsonify('Muscle Mass', 1, [w.date for w in weighins], [str(w.muscle_mass) for w in weighins], "#89A54E", True) + "]}"
        return final_json


def jsonify(name, axis, xData, yData, color, dashed=False, ):
    json = "{\"name\":\"" + name + "\""
    json += ", \"connectNulls\": true"
    json += ", \"color\":\"" + color + "\""
    if dashed:
        json += ", \"dashStyle\": \"shortdot\""
    json += ", \"yAxis\":" + str(axis)
    json += ", \"data\": ["
    for x, y in zip(xData, yData):
        if float(y) == 0:
            json += "[null,null],"
        else:
            json += "[" + x.strftime('%m/%d/%Y') + "," + y + "],"
    json = json[:-1] + "]}"
    return json