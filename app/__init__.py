#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" module """

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'somerandomkey'


# Jinja functions
def getRowColor(quantity):
    quantity = int(quantity)
    if quantity <= 100:
        return "table-danger"
    elif quantity <= 500:
        return "table-warning"


app.jinja_env.globals.update(getRowColor=getRowColor)

from app import routes
