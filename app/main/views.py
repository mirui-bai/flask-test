from flask import render_template, session, redirect, url_for, current_app
from datetime import datetime

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
from flask import current_app


@main.route('/<name>')
def user(name):
    return render_template("user.html", name=name)


@main.route('/', methods=["Get", "Post"])
def index():
    app = current_app._get_current_object()

    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known=session.get('known', False)
                           )


