from Main.decorators import crossdomain
from ..util import session
from ..models import *
import flask
import flask.views


class TagsAPI(flask.views.MethodView):

    @crossdomain(origin='*')
    def get(self, tag_id):
        if tag_id is None:
            tag_filter = flask.request.args.get('q')
            tag_list = []

            if not tag_filter:
                tags = session.query(Tag).limit(10)
            else:
                tags = session.query(Tag).filter(Tag.name.contains(tag_filter)).limit(10)

            for tag in tags:
                tag_list.append({'id': str(tag.id), 'text': tag.name})

            return flask.jsonify(tags=tag_list)
        else:
            pass
