from mangum import Mangum

from app import db
from app.main import app


handler = Mangum(app, lifespan='off')
