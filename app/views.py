from app import app
from flask import render_template
from forms import NameForm

from flask import Flask, render_template, session, redirect, url_for,flash

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'hello flask'
