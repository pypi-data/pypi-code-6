#!/usr/bin/python
# -*- coding: utf-8 -*-


from flask import Blueprint, got_request_exception, current_app
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()
mod = Blueprint('models', __name__)


def init_app(app):
    db.init_app(app)
    app.register_blueprint(mod)
    got_request_exception.connect_via(app)(got_request_exception_handler)


@mod.after_app_request
def after_app_request(f):
    if current_app.config.get('COMMIT_ON_AFTER_REQUEST', True):  # pragma: no cover
        db.session.commit()
    return f


def got_request_exception_handler(sender, exception, **extras):
    db.session.rollback()  # pragma: no cover


class Testimonial(db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.Integer, primary_key=True)
    approved = db.Column(db.Boolean, nullable=False)
    sender_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    company_url = db.Column(db.String(2000), nullable=False)
    company_logo = db.Column(db.String(2000), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(2000))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
