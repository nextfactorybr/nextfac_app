from flask import Blueprint, request, render_template, make_response, redirect, url_for
from models.project import Project
from models.shift import Shift

project_blueprints = Blueprint("projects", __name__)


@project_blueprints.route('/')
def index():
    projects = Project.all()
    return render_template('projects/index.html', projects=projects)


@project_blueprints.route('/search', methods=['POST'])
def search():
    if request.method == 'POST' and request.form['parameter'] != "":
        parameter = request.form['parameter']
        projects = Project.get_by_search(parameter)
        return render_template('projects/index.html', projects=projects)
    else:
        return redirect(url_for('projects.index'))


@project_blueprints.route('/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        weight = request.form['weight']
        shift_id = request.form['shift_id']
        path = request.form['path']

        Project(name, time, weight, shift_id, path).save_to_mongo()
        return redirect(url_for('projects.index'))
    else:
        shifts = Shift.all()
        return render_template('projects/new_project.html', shifts=shifts)


@project_blueprints.route('/edit/<string:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.get_by_id(project_id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.time = request.form['time']
        project.weight = request.form['weight']
        project.shift_id = request.form['shift_id']
        project.path = request.form['path']

        project.save_to_mongo()
        return redirect(url_for('projects.index'))
    else:
        return render_template('projects/edit_project.html', project=project)


@project_blueprints.route('/delete/<string:project_id>', methods=['GET'])
def remove_project(project_id):
    project = Project.get_by_id(project_id)
    project.remove_from_mongo()

    return redirect(url_for('projects.index'))
