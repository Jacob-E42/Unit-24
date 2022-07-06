"""models app for cupcakes"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

DEFAULT_IMAGE = "https://tinyurl.com/demo-cupcake"

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE)

    def __repr__(self):
        c = self
        return f" {self.id} {c.flavor} {c.size} {c.rating} {c.image} "

    def serialize(self):
        """Instance method that returns a dict of a row's data to make it JSON compatible"""

        c = self
        return {
            "id": c.id,
            "flavor": c.flavor,
            "size": c.size,
            "rating": c.rating,
            "image": c.image
        }
