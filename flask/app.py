from flask import Flask, redirect, url_for, request, render_template, make_response, session, abort, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.secret_key = 'XYZ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:donghm@127.0.0.1/automation'

db = SQLAlchemy(app)

class Human(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    city = db.Column(db.String(255))

    def __init__(self, name, address, city):
        self.name = name
        self.address = address
        self.city = city

@app.route('/address')
def address():
    db.create_all()
    return render_template('address.html')


@app.route('/show_all')
def show_all():
    # return render_template('show_all.html')
    human = Human.query.all()
    print(human)
    return render_template('show_all.html', human = human)


@app.route('/show_update', methods=['POST', 'GET'])
def show_update():
    id = request.args.get('id')
    human = AddressBook.query.filter_by(id=id).first()
    return render_template('update_addr.html', address=address)

@app.route('/new_addr', methods=['POST', 'GET'])
def new_addr():
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['address'])
        print(request.form['city'])
        name = request.form['name']
        h = Human(request.form['name'], request.form['address'],request.form['city'])
        db.session.add(h)
        db.session.commit()
    return render_template('show_all.html', human = Human.query.all())
    # return render_template('show_all.html', addresses = AddressBook.query.all())

@app.route('/delete_addr')
def delete_addr():
    id = request.args.get('id')
    address = AddressBook.query.filter_by(id=id).first()
    db.session.delete(address)
    db.session.commit()
    return render_template('show_all.html', addresses = AddressBook.query.all())


@app.route('/update_addr', methods=['POST', 'GET'])
def update_addr():
    if request.method == 'POST':
        print "Inside POST"
        try:
            id = request.form['id']
            address = AddressBook.query.filter_by(id=id).first()
            address.name = request.form['name']
            address.addr = request.form['address']
            address.city = request.form['city']
            db.session.commit()
        except:
            msg = "error during update operation"
            print msg
    return render_template('show_all.html', addresses = AddressBook.query.all())