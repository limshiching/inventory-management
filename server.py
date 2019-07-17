import peeweedbevolve
from flask import Flask, render_template, request, redirect,url_for, flash
from models import db, Store, Warehouse

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

@app.route('/stores')
def store_display():
    stores = Store.select()
    return render_template('stores.html',stores=stores)

@app.route('/warehouse')
def warehouse_new():
    stores = Store.select() # PUT IN HERE AS NEED TO RENDER TEMPLATE, NOT IN WAREHOUSE HTML
    return render_template('warehouse.html',stores=stores)


@app.route('/warehouse/create', methods=["POST"])
def warehouse_create():
    # print(request.form['store_id'])
    store = Store.get_by_id(request.form['store_id'])
    w = Warehouse(location=request.form['warehouse_location'], store=store)
    w.save()
    return redirect(url_for ('warehouse_new'))


if __name__ == '__main__':
    app.run()
