from flask import Blueprint, request, render_template, make_response, redirect, url_for
from models.filament import Filament

filament_blueprints = Blueprint("filaments", __name__)


@filament_blueprints.route('/')
def index():
    filaments = Filament.all()
    return render_template('filaments/index.html', filaments=filaments)


@filament_blueprints.route('/new', methods=['GET', 'POST'])
def new_filament():
    if request.method == 'POST':
        cor = request.form['cor']
        temp = request.form['temp']
        filament_type = request.form['filament_type']
        provider = request.form['provider']
        cost = request.form['cost']
        quality = request.form['quality']
        stock = request.form['stock']
        weight = request.form['weight']
        name = filament_type + "-" + cor + " " + provider + "-" + weight

        Filament(cor, temp, filament_type, provider, cost, quality, stock, weight, name).save_to_mongo()
        return redirect(url_for('filaments.index'))
    else:
        return render_template('filaments/new_filament.html')


@filament_blueprints.route('/edit/<string:filament_id>', methods=['GET', 'POST'])
def edit_filament(filament_id):
    filament = Filament.get_by_id(filament_id)

    if request.method == 'POST':
        filament.cor = request.form['cor']
        filament.temp = request.form['temp']
        filament.filament_type = request.form['filament_type']
        filament.cost = request.form['cost']
        filament.quality = request.form['quality']
        filament.stock = request.form['stock']
        filament.weight = request.form['weight']
        filament.name = filament.filament_type + "-" + filament.cor + " " + filament.provider + "-" + filament.weight

        filament.save_to_mongo()
        return redirect(url_for('filaments.index'))
    else:
        return render_template('filaments/edit_filament.html', filament=filament)


@filament_blueprints.route('/delete/<string:filament_id>', methods=['GET'])
def remove_filament(filament_id):
    filament = Filament.get_by_id(filament_id)
    filament.remove_from_mongo()

    return redirect(url_for('filaments.index'))
