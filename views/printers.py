from flask import Blueprint, request, render_template, make_response, redirect, url_for

from models.printer import Printer

printer_blueprints = Blueprint("printers", __name__)


@printer_blueprints.route('/')
def index():
    printers = Printer.all()
    return render_template('printers/index.html', printers=printers)


@printer_blueprints.route('/new', methods=['GET', 'POST'])
def new_printer():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        apikey = request.form['apikey']

        Printer(name, url, apikey).save_to_mongo()
        return redirect(url_for('printers.index'))
    else:
        return render_template('printers/new_printer.html')


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
        return render_template('printers/edit_printer.html', printer=printer)


@printer_blueprints.route('/delete/<string:printer_id>', methods=['GET'])
def remove_printer(printer_id):
    printer = Printer.get_by_id(printer_id)
    printer.remove_from_mongo()

    return redirect(url_for('printers.index'))
