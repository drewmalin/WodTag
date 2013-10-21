from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from Main import app

engine = create_engine('sqlite:///WodTag.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

lm = LoginManager()
lm.init_app(app)