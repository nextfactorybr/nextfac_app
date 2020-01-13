from flask import Blueprint, request, render_template, make_response, redirect, url_for
from models.shift import Shift

shift_blueprints = Blueprint("shifts", __name__)


@shift_blueprints.route('/')
def index():
    shifts = Shift.all()
    return render_template('shifts/index.html', shifts=shifts)


@shift_blueprints.route('/new', methods=['GET', 'POST'])
def new_shift():
    if request.method == 'POST':
        desc = request.form['desc']
        timein = request.form['timein']
        timeout = request.form['timeout']

        Shift(desc, timein, timeout).save_to_mongo()
        return redirect(url_for('shifts.index'))
    else:
        return render_template('shifts/new_shift.html')


@shift_blueprints.route('/edit/<string:shift_id>', methods=['GET', 'POST'])
def edit_shift(shift_id):
    shift = Shift.get_by_id(shift_id)

    if request.method == 'POST':
        shift.desc = request.form['desc']
        shift.timein = request.form['timein']
        shift.timeout = request.form['timeout']

        shift.save_to_mongo()
        return redirect(url_for('shifts.index'))
    else:
        return render_template('shifts/edit_shift.html', shift=shift)


@shift_blueprints.route('/delete/<string:shift_id>', methods=['GET'])
def remove_shift(shift_id):
    shift = Shift.get_by_id(shift_id)
    shift.remove_from_mongo()

    return redirect(url_for('shifts.index'))
