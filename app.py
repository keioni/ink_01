#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    A Study for Flask and Flask-Login.

    by Kei Onimaru <otegami@devel.keys.jp>
"""

from flask import Flask
from flask import request, redirect


app = Flask(__name__)
app.config.from_envvar('FLASK_SETTINGS', silent=True)

@app.route('/')
def path_route():
    return redirect('https://ink.keys.jp/api/')

@app.route('/token', methods=['POST', 'DELETE'])
def path_token():
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

@app.route('/boxes', methods=['GET', 'POST', 'DELETE'])
def path_boxes():
    pass

@app.route('/cards', methods=['GET', 'POST', 'DELETE'])
def path_cards():
    pass

@app.route('/cards/<int:card_id>/records', methods=['GET', 'POST', 'DELETE'])
def path_records(card_id: int):
    pass
