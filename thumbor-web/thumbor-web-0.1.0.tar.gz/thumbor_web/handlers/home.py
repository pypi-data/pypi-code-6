#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import markdown

from thumbor_web import models


mod = Blueprint('home', __name__)


@mod.route("/", methods=['GET'])
def show():
    return render_template('index.html')


@mod.route("/testimonials", methods=['GET'])
def testimonials():
    testimonials = models.Testimonial.query.filter_by(approved=True).order_by(models.Testimonial.order).all()
    return render_template('testimonials_page.html', testimonials=testimonials)


@mod.route("/new-testimonial", methods=['POST'])
def new_testimonial():
    testimonial = models.Testimonial(
        approved=False,
        sender_name=request.form['sender_name'],
        email=request.form['email'],
        company_name=request.form['company_name'],
        company_url=request.form['company_url'],
        company_logo=None,
        summary=None,
        text=markdown.markdown(request.form['testimonial']),
        order=0
    )
    models.db.session.add(testimonial)
    models.db.session.flush()

    return "OK"
