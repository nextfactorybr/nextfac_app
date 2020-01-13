from flask import Flask

from models import helpers
from views.jobs import job_blueprints
from views.printers import printer_blueprints
from views.shifts import shift_blueprints
from views.project import project_blueprints
from views.filaments import filament_blueprints

app = Flask(__name__)
app.register_blueprint(printer_blueprints, url_prefix="/printers")
app.register_blueprint(shift_blueprints, url_prefix="/shifts")
app.register_blueprint(project_blueprints, url_prefix="/projects")
app.register_blueprint(filament_blueprints, url_prefix="/filaments")
app.register_blueprint(job_blueprints, url_prefix="/jobs")
app.jinja_env.globals['static'] = helpers.static_file

if __name__ == '__main__':
    app.run(host='192.168.0.127', debug=True)
