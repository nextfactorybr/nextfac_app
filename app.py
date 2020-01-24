import os

from flask import Flask, render_template

from models import helpers
from views.jobs import job_blueprints
from views.printers import printer_blueprints
from views.shifts import shift_blueprints
from views.projects import project_blueprints
from views.filaments import filament_blueprints
from views.users import user_blueprints

app = Flask(__name__)
app.secret_key = 'cd48e1c22de0961d5d1bfb14f8a66e006cfb1cfbf3f0c0f3'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(printer_blueprints, url_prefix="/printers")
app.register_blueprint(shift_blueprints, url_prefix="/shifts")
app.register_blueprint(project_blueprints, url_prefix="/projects")
app.register_blueprint(filament_blueprints, url_prefix="/filaments")
app.register_blueprint(job_blueprints, url_prefix="/jobs")
app.register_blueprint(user_blueprints, url_prefix="/auth")
app.jinja_env.globals['static'] = helpers.static_file

if __name__ == '__main__':
    app.run(host='nextfactory.casaz.com.br', port=80, debug=True)
