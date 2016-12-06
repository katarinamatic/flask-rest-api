from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger_2 import Api
import logging
from flask_cors import CORS


app = Flask('cvquery')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza-podataka.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

api = Api(app, api_spec_url='/docs')
CORS(app)

#za log
logger = logging.getLogger('app')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('reqs.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)