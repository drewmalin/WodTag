from util import Base, lm, session
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
import hashlib
import random

###
# Many-to-many joiner table (WorkoutPart >--< Tag)
#
tag_part_association = Table('tag_part_association', Base.metadata,
                             Column('part_id', Integer, ForeignKey('WorkoutPart.id')),
                             Column('tag_id', Integer, ForeignKey('Tag.id')))

###
# Many-to-many joiner table (WorkoutResult >---< Tag)
#
tag_result_association = Table('tag_result_association', Base.metadata,
                               Column('result_id', Integer, ForeignKey('WorkoutResult.id')),
                               Column('tag_id', Integer, ForeignKey('Tag.id')))


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(128))
    password = Column(String(128))
    salt = Column(String(128))
    is_gym_owner = Column(Boolean)
    member_gym_id = Column(Integer, ForeignKey('Gym.id'))
    owner_gym_id = Column(Integer, ForeignKey('Gym.id'))

    def __init__(self, username, password):
        self.username = username
        self.salt = hashlib.md5(str(random.random())).hexdigest()
        self.password = hashlib.sha1(password + self.salt).hexdigest()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

@lm.user_loader
def load_user(user_id):
    return session.query(User).filter_by(id=int(user_id)).first()

class Gym(Base):
    __tablename__ = 'Gym'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(String(512))

    owners = relationship('User', backref='owns_gym', foreign_keys="User.owner_gym_id")
    members = relationship('User', backref='member_of_gym', foreign_keys="User.member_gym_id")
    template_workouts = relationship('Workout', backref='gym', order_by='Workout.post_date.desc()')

    def __init__(self, name, description):
        self.name = name
        self.description = description

###
# Acts as a template for workout results. Gyms create and own templated workouts,
# which can be used to generate user-specific results. Workout templates are made
# up of at least one part
#
class Workout(Base):
    __tablename__ = 'Workout'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    post_date = Column(DateTime)
    gym_id = Column(Integer, ForeignKey('Gym.id'))

    parts = relationship('WorkoutPart', backref='workout', order_by='WorkoutPart.order')
    results = relationship('WorkoutResult', backref='workout')

    def __init__(self, name):
        self.name = name

###
# Pieces of a workout. Workouts are generally made up of two or three parts
#
class WorkoutPart(Base):
    __tablename__ = 'WorkoutPart'
    id = Column(Integer, primary_key=True)

    description = Column(String(512))
    workout_id = Column(Integer, ForeignKey('Workout.id'))
    order = Column(String(64))
    uom = Column(String(128))

    def __init__(self, description):
        self.description = description

###
# Workout results are owned by users
#
class WorkoutResult(Base):
    __tablename__ = 'WorkoutResult'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('User.id'))
    workout_id = Column(Integer, ForeignKey('Workout.id'))
    user = relationship('User', backref='results')
    parts = relationship('WorkoutPartResult', backref='workout_result')

###
# Workout part results are owned by WorkoutResults
#
class WorkoutPartResult(Base):
    __tablename__ = 'WorkoutPartResult'
    id = Column(Integer, primary_key=True)
    result = Column(String(128))
    details = Column(String(512))

    part_id = Column(Integer, ForeignKey('WorkoutPart.id'))
    part = relationship('WorkoutPart', backref='results')
    result_id = Column(Integer, ForeignKey('WorkoutResult.id'))

    def __init__(self, result):
        self.result = result


###
# Assigned directly to workout results by users or to workout parts by gyms
class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    parts = relationship('WorkoutPart', secondary=tag_part_association, backref='tags')
    results = relationship('WorkoutResult', secondary=tag_result_association, backref='tags')

    def __init__(self, name):
        self.name = name
