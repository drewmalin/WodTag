from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'under_development'

# There must be a better way than this!
from Main.views.index import *
from Main.views.user import *
from Main.views.gym import *
from Main.views.workout import *
from Main.views.result import *
from Main.views.api import *

## ------------ INDEX -------------- ##
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET', 'POST'])

## ------------ USER -------------- ##
app.add_url_rule('/user/',
                 defaults={'user_id': None},
                 view_func=UserView.as_view('user'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/<int:user_id>',
                 view_func=UserView.as_view('known_user'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/edit',
                 defaults={'user_id': None},
                 view_func=UserMod.as_view('user_mod'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/edit/<int:user_id>',
                 view_func=UserMod.as_view('known_user_mod'),
                 methods=['GET', 'POST'])

## ------------ GYM -------------- ##
app.add_url_rule('/all_gyms/',
                 view_func=AllGymsView.as_view('all_gyms'),
                 methods=['GET'])
app.add_url_rule('/gym/',
                 defaults={'gym_id': None},
                 view_func=GymView.as_view('gym'),
                 methods=['GET', 'POST'])
app.add_url_rule('/gym/<int:gym_id>',
                 view_func=GymView.as_view('known_gym'),
                 methods=['GET', 'POST'])
app.add_url_rule('/gym/edit',
                 defaults={'gym_id': None},
                 view_func=GymMod.as_view('gym_mod'),
                 methods=['GET', 'POST'])
app.add_url_rule('/gym/edit/<int:gym_id>',
                 view_func=GymMod.as_view('known_gym_mod'),
                 methods=['GET', 'POST'])
app.add_url_rule('/workout_template/<int:workout_template_id>',
                 view_func=WorkoutTemplateView.as_view('workout_template'),
                 methods=['GET'])
app.add_url_rule('/workout_template/edit/',
                 view_func=WorkoutTemplateMod.as_view('workout_template_mod'),
                 methods=['GET', 'POST'])
app.add_url_rule('/workout_template/<int:workout_template_id>/results/',
                 view_func=WorkoutTemplateResults.as_view('workout_template_results'),
                 methods=['GET'])
app.add_url_rule('/gym/<int:gym_id>/members/',
                 view_func=AllGymMembersView.as_view('gym_members'),
                 methods=['GET'])
app.add_url_rule('/gym/<int:gym_id>/owners/',
                 view_func=AllGymOwnersView.as_view('gym_owners'),
                 methods=['GET'])

## ------------ WORKOUT -------------- ##
app.add_url_rule('/result/',
                 defaults={'result_id': None},
                 view_func=ResultView.as_view('result'),
                 methods=['GET', 'POST'])
app.add_url_rule('/result/<int:result_id>',
                 view_func=ResultView.as_view('known_result'),
                 methods=['GET', 'POST'])
app.add_url_rule('/result/edit/',
                 defaults={'result_id': None},
                 view_func=ResultMod.as_view('result_mod'),
                 methods=['GET', 'POST'])
app.add_url_rule('/result/edit/<int:workout_id>',
                 view_func=ResultMod.as_view('known_result_mod'),
                 methods=['GET', 'POST'])

## -------------- API ---------------- ##

app.add_url_rule('/api/tags/',
                 defaults={'tag_id': None},
                 view_func=TagsAPI.as_view('tags_api'),
                 methods=['GET'])
app.add_url_rule('/api/tags/<int:tag_id>',
                 view_func=TagsAPI.as_view('known_tags_api'),
                 methods=['GET'])

## ------------ DB Init -------------- ##
from util import Base, engine
from models import *
Base.metadata.create_all(engine)

## ----------- Seed Data ------------- ##
f = open("Main/data/tags.txt", "r")
data = f.readlines()
for line in data:
    line = line.strip()
    tag = session.query(Tag).filter_by(name=line).first()
    if tag is None:
        tag = Tag(line)
    session.add(tag)
session.commit()