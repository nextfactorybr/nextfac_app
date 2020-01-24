from flask import Blueprint, request, render_template, make_response, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from models.shift import Shift
from models.user.decorators import requires_login, requires_admin

shift_blueprints = Blueprint("shifts", __name__)

view = {
            "title": "Shifts",
            "icon": "fa-print",
            "name": "shifts",
            "nav_on": True,
            "search_on": False
        }


@shift_blueprints.route('/')
@requires_login
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 6
    offset = (page - 1) * per_page

    shifts = Shift.all(offset, per_page)
    counter = len(Shift.all())

    view['title'] = "Shifts"
    view['search_on'] = True

    search = False
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, per_page=per_page, css_framework='bootstrap4', offset=offset, total=counter,
                            search=search, record_name='shifts')

    return render_template('shifts/index.html', shifts=shifts, pagination=pagination, view=view)


@shift_blueprints.route('/new', methods=['GET', 'POST'])
@requires_login
def new_shift():
    if request.method == 'POST':
        desc = request.form['desc']
        timein = request.form['timein']
        timeout = request.form['timeout']

        Shift(desc, timein, timeout).save_to_mongo()
        return redirect(url_for('shifts.index'))
    else:
        view['title'] = "New shift"
        view['search_on'] = False
        return render_template('shifts/new_shift.html', view=view)


@shift_blueprints.route('/edit/<string:shift_id>', methods=['GET', 'POST'])
@requires_login
def edit_shift(shift_id):
    shift = Shift.get_by_id(shift_id)

    if request.method == 'POST':
        shift.desc = request.form['desc']
        shift.timein = request.form['timein']
        shift.timeout = request.form['timeout']

        shift.save_to_mongo()
        return redirect(url_for('shifts.index'))
    else:
        view['title'] = "Edit shift"
        view['search_on'] = False
        return render_template('shifts/edit_shift.html', shift=shift, view=view)


@shift_blueprints.route('/delete/<string:shift_id>', methods=['GET'])
@requires_login
def remove_shift(shift_id):
    shift = Shift.get_by_id(shift_id)
    shift.remove_from_mongo()

    return redirect(url_for('shifts.index'))


@shift_blueprints.route('/search', methods=['POST'])
@requires_login
def search():
    if request.method == 'POST' and request.form['parameter'] != "":
        parameter = request.form['parameter']
        shifts = Shift.get_by_search(parameter)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        counter = len(shifts)
        per_page = counter if counter > 0 else 1
        offset = counter

        view['title'] = "Shifts"
        view['search_on'] = True

        search = False
        q = request.args.get('q')
        if q:
            search = True

        pagination = Pagination(page=page, per_page=per_page, css_framework='bootstrap4', offset=offset, total=counter,
                                search=search, record_name='shifts')

        return render_template('shifts/index.html', shifts=shifts, pagination=pagination, view=view)
    else:
        return redirect(url_for('shifts.index'))
