from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db


def add_schema(cls):
    class Schema(SQLAlchemyAutoSchema):
        class Meta:
            model = cls
            load_instance = True

    cls.Schema = Schema
    return cls


class BaseModel(db.Model):
    __abstract__ = True

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '{}'.format(self.id)


@add_schema
class Trade(BaseModel):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(3), nullable=False)
    matched_price = db.Column(db.Float, nullable=False)
    average_price = db.Column(db.Float, nullable=True)
    net_price = db.Column(db.Float, nullable=False)
    shares = db.Column(db.Float, nullable=False)
    order = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def dump(self):
        return __class__.Schema().dump(self)

    @staticmethod
    def load(data):
        return __class__.Schema().load(data, session=db.session)


@add_schema
class Stock(BaseModel):
    __tablename__ = 'stocks'

    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(3), unique=Trade)
    price = db.Column(db.Float, default=0)
    shares = db.Column(db.Float, default=0)
    ratio = db.Column(db.Float, default=0.2)
    freeroll = db.Column(db.Boolean, default=False)

    def dump(self):
        return __class__.Schema().dump(self)

    @staticmethod
    def load(data):
        return __class__.Schema().load(data, session=db.session)


@add_schema
class Note(BaseModel):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True)
    content = db.Column(db.Text())
    visited = db.Column(db.Integer, default=0)

    def dump(self):
        return __class__.Schema().dump(self)

    @staticmethod
    def load(data):
        return __class__.Schema().load(data, session=db.session)
