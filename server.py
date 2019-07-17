import peeweedbevolve
from flask import Flask, render_template, request, redirect,url_for
from models import db, Store

app = Flask(__name__)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response


@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})


@app.route("/")
def index():
    store_name = request.args.get("store_name")
    return render_template('index.html', store_name=store_name)


@app.route('/store')
def store_new():
    return render_template('store.html')


@app.route('/store/create', methods=["POST"])
def store_create():
    store_name = request.form['store_name']
    s = Store(name=store_name)
    s.save()
    return redirect(url_for('store_new'))


if __name__ == '__main__':
    app.run()
