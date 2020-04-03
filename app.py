import os

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_dropzone import Dropzone
from models import helpers
from views.jobs import job_blueprints
from views.printers import printer_blueprints
from views.shifts import shift_blueprints
from views.projects import project_blueprints
from views.filaments import filament_blueprints
from views.users import user_blueprints
from flask_wtf.csrf import CSRFProtect

base_path = os.path.abspath(os.path.dirname(__file__))
upload_path = os.path.join(base_path, 'static/gcodes/files/')
temp_path = os.path.join(base_path, 'static/gcodes/temporal/')

app = Flask(__name__)
dropzone = Dropzone(app)
#csrf = CSRFProtect(app)
app.secret_key = 'cd48e1c22de0961d5d1bfb14f8a66e006cfb1cfbf3f0c0f3'
#app.config['DROPZONE_ENABLE_CSRF'] = True   #CSRF Protection Enabled
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True  # enable parallel upload
app.config['DROPZONE_PARALLEL_UPLOADS'] = 3  # handle 3 file per request
app.config.update(
    ADMIN=os.environ.get('ADMIN'),
    UPLOAD_FOLDER=upload_path,
    TEMPORAL_FOLDER=temp_path
)


@app.route('/')
def home():
    if 'email' in session:
        if session['email'] is not None:
            return redirect(url_for('jobs.index'))

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
