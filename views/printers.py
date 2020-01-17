from flask import Blueprint, request, render_template, make_response, redirect, url_for
from flask_paginate import Pagination, get_page_parameter
from models.printer import Printer

printer_blueprints = Blueprint("printers", __name__)

view = {
            "title": "Printers",
            "icon": "fa-print",
            "name": "printers",
            "nav_on": True,
            "search_on": False
        }


@printer_blueprints.route('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)

    per_page = 6
    offset = (page - 1) * per_page

    printers = Printer.all(offset, per_page)
    counter = len(Printer.all())

    view['title'] = "Printers"
    view['search_on'] = True

    search = False
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, per_page=per_page, css_framework='bootstrap4', offset=offset, total=counter,
                            search=search, record_name='printers')

    return render_template('printers/index.html', printers=printers, pagination=pagination, view=view)


@printer_blueprints.route('/new', methods=['GET', 'POST'])
def new_printer():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        apikey = request.form['apikey']

        Printer(name, url, apikey).save_to_mongo()
        return redirect(url_for('printers.index'))
    else:
        view['title'] = "New printer"
        view['search_on'] = False
        return render_template('printers/new_printer.html', view=view)


@printer_blueprints.route('/edit/<string:printer_id>', methods=['GET', 'POST'])
def edit_printer(printer_id):
    printer = Printer.get_by_id(printer_id)

    if request.method == 'POST':
        printer.name = request.form['name']
        printer.url = request.form['url']
        printer.apikey = request.form['apikey']

        printer.save_to_mongo()
        return redirect(url_for('printers.index'))
    else:
        view['title'] = "Edit printer"
        view['search_on'] = False
        return render_template('printers/edit_printer.html', printer=printer, view=view)


@printer_blueprints.route('/delete/<string:printer_id>', methods=['GET'])
def remove_printer(printer_id):
    printer = Printer.get_by_id(printer_id)
    printer.remove_from_mongo()

    return redirect(url_for('printers.index'))


@printer_blueprints.route('/search', methods=['POST'])
def search():
    if request.method == 'POST' and request.form['parameter'] != "":
        parameter = request.form['parameter']
        printers = Printer.get_by_search(parameter)

        page = request.args.get(get_page_parameter(), type=int, default=1)
        counter = len(printers)
        per_page = counter if counter > 0 else 1
        offset = counter

        view['title'] = "Printers"
        view['search_on'] = True

        search = False
        q = request.args.get('q')
        if q:
            search = True

        pagination = Pagination(page=page, per_page=per_page, css_framework='bootstrap4', offset=offset, total=counter,
                                search=search, record_name='printers')

        return render_template('printers/index.html', printers=printers, pagination=pagination, view=view)
    else:
        return redirect(url_for('printers.index'))
