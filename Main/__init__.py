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
from Main.views.search import *

## ------------ INDEX -------------- ##
app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=['GET', 'POST'])

## ------------ USER -------------- ##
app.add_url_rule('/users/',
                 view_func=Users.as_view('users'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/<int:user_id>',
                 view_func=UserCRUD.as_view('user'),
                 methods=['GET', 'POST'])
app.add_url_rule('/user/create',
                 view_func=UserCreate.as_view('user_create'),
                 methods=['GET'])
app.add_url_rule('/user/edit/<int:user_id>',
                 view_func=UserEdit.as_view('user_edit'),
                 methods=['GET'])

## ------------ GYM -------------- ##
app.add_url_rule('/gyms/',
                 view_func=Gyms.as_view('gyms'),
                 methods=['GET', 'POST'])
app.add_url_rule('/gym/<int:gym_id>',
                 view_func=GymCRUD.as_view('gym'),
                 methods=['GET', 'POST'])
app.add_url_rule('/gym/create',
                 view_func=GymCreate.as_view('gym_create'),
                 methods=['GET'])
app.add_url_rule('/gym/edit/<int:gym_id>',
                 view_func=GymEdit.as_view('gym_edit'),
                 methods=['GET'])
app.add_url_rule('/gym/<int:gym_id>/members/',
                 view_func=AllGymMembersView.as_view('gym_members'),
                 methods=['GET'])
app.add_url_rule('/gym/<int:gym_id>/owners/',
                 view_func=AllGymOwnersView.as_view('gym_owners'),
                 methods=['GET'])

## -------------- WORKOUT ----------------- ##
app.add_url_rule('/workouts/',
                 view_func=Workouts.as_view('workouts'),
                 methods=['GET', 'POST'])
app.add_url_rule('/workout/<int:workout_id>',
                 view_func=WorkoutCRUD.as_view('workout'),
                 methods=['GET', 'POST'])
app.add_url_rule('/workout/create',
                 view_func=WorkoutCreate.as_view('workout_create'),
                 methods=['GET'])
app.add_url_rule('/workout/edit/<int:workout_id>',
                 view_func=WorkoutEdit.as_view('workout_edit'),
                 methods=['GET'])
app.add_url_rule('/workout_template/<int:workout_id>/results/',
                 view_func=WorkoutResults.as_view('workout_results'),
                 methods=['GET'])

## -------------- RESULTS -------------- ##
app.add_url_rule('/results/',
                 view_func=Results.as_view('results'),
                 methods=['GET', 'POST'])
app.add_url_rule('/result/<int:result_id>',
                 view_func=ResultCRUD.as_view('result'),
                 methods=['GET', 'POST'])
app.add_url_rule('/result/create/<int:workout_id>',
                 view_func=ResultCreate.as_view('result_create'),
                 methods=['GET'])
app.add_url_rule('/result/edit/<int:result_id>',
                 view_func=ResultEdit.as_view('result_edit'),
                 methods=['GET'])

## -------------- API ---------------- ##
app.add_url_rule('/api/tags/',
                 defaults={'tag_id': None},
                 view_func=TagsAPI.as_view('tags_api'),
                 methods=['GET'])
app.add_url_rule('/api/tags/<int:tag_id>',
                 view_func=TagsAPI.as_view('known_tags_api'),
                 methods=['GET'])

## ------------- SEARCH ---------------##
app.add_url_rule('/search/',
                 view_func=SearchView.as_view('search'),
                 methods=['GET', 'POST'])

## ------------ DB Init -------------- ##
from util import db
from models import *
db.create_all()

## ----------- Seed Data ------------- ##
f = open("Main/data/tags.txt", "r")
data = f.readlines()
for line in data:
    line = line.strip()
    tag = Tag.query.filter_by(name=line).first()
    if tag is None:
        tag = Tag(line)
    db.session.add(tag)
db.session.commit()