from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Darboviete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(100), nullable=False)
    miestas = db.Column(db.String(100), nullable=False)
    darbuotoju_skaicius = db.Column(db.Integer, nullable=False)
    darbuotojai = db.relationship('Darbuotojas', backref='darboviete', lazy=True)


class Darbuotojas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column(db.String(100), nullable=False)
    pavarde = db.Column(db.String(100), nullable=False)
    pareigos = db.Column(db.String(100), nullable=False)
    darboviete_id = db.Column(db.Integer, db.ForeignKey('darboviete.id'), nullable=False)


@app.route('/')
def index():
    darbovietes = Darboviete.query.all()
    return render_template('index.html', darbovietes=darbovietes)


@app.route('/prideti-darboviete', methods=['GET', 'POST'])
def prideti_darboviete():
    if request.method == 'POST':
        pavadinimas = request.form['pavadinimas']
        miestas = request.form['miestas']
        darbuotoju_skaicius = request.form['darbuotoju_skaicius']

        nauja_darboviete = Darboviete(pavadinimas=pavadinimas, miestas=miestas, darbuotoju_skaicius=darbuotoju_skaicius)
        db.session.add(nauja_darboviete)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('addworkplace.html')


@app.route('/redaguoti-darboviete/<int:id>', methods=['GET', 'POST'])
def redaguoti_darboviete(id):
    darboviete = Darboviete.query.get_or_404(id)

    if request.method == 'POST':
        darboviete.pavadinimas = request.form['pavadinimas']
        darboviete.miestas = request.form['miestas']
        darboviete.darbuotoju_skaicius = request.form['darbuotoju_skaicius']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editworkplace.html', darboviete=darboviete)


@app.route('/trinti-darboviete/<int:id>', methods=['GET', 'POST'])
def trinti_darboviete(id):
    darboviete = Darboviete.query.get_or_404(id)

    if darboviete.darbuotojai:
        return redirect(url_for('index'))

    db.session.delete(darboviete)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/darbuotojai')
def darbuotojai():
    darbuotojai = Darbuotojas.query.all()
    return render_template('employees.html', darbuotojai=darbuotojai)


@app.route('/prideti-darbuotoja', methods=['GET', 'POST'])
def prideti_darbuotoja():
    darbovietes = Darboviete.query.all()

    if request.method == 'POST':
        vardas = request.form['vardas']
        pavarde = request.form['pavarde']
        pareigos = request.form['pareigos']
        darboviete_id = request.form['darboviete_id']

        naujas_darbuotojas = Darbuotojas(vardas=vardas, pavarde=pavarde, pareigos=pareigos, darboviete_id=darboviete_id)
        db.session.add(naujas_darbuotojas)
        db.session.commit()
        return redirect(url_for('darbuotojai'))

    return render_template('addemployee.html', darbovietes=darbovietes)


@app.route('/redaguoti-darbuotoja/<int:id>', methods=['GET', 'POST'])
def redaguoti_darbuotoja(id):
    darbuotojas = Darbuotojas.query.get_or_404(id)
    darbovietes = Darboviete.query.all()

    if request.method == 'POST':
        darbuotojas.vardas = request.form['vardas']
        darbuotojas.pavarde = request.form['pavarde']
        darbuotojas.pareigos = request.form['pareigos']
        darbuotojas.darboviete_id = request.form['darboviete_id']
        db.session.commit()
        return redirect(url_for('darbuotojai'))

    return render_template('editemployee.html', darbuotojas=darbuotojas, darbovietes=darbovietes)


@app.route('/trinti-darbuotoja/<int:id>', methods=['GET', 'POST'])
def trinti_darbuotoja(id):
    darbuotojas = Darbuotojas.query.get_or_404(id)
    db.session.delete(darbuotojas)
    db.session.commit()
    return redirect(url_for('darbuotojai'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)