from flask import Blueprint, render_template, request, redirect, url_for
from app import mongo
from bson.objectid import ObjectId

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    projects = mongo.db.projects.find()
    return render_template('index.html', projects=projects)

@bp.route('/project/<id>')
def project(id):
    project = mongo.db.projects.find_one({"_id": ObjectId(id)})
    return render_template('project.html', project=project)

@bp.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project = {
            'name': request.form['name'],
            'description': request.form['description']
        }
        mongo.db.projects.insert_one(project)
        return redirect(url_for('main.index'))
    return render_template('add_project.html')

@bp.route('/update/<id>', methods=['GET', 'POST'])
def update_project(id):
    project = mongo.db.projects.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        updated_project = {
            'name': request.form['name'],
            'description': request.form['description']
        }
        mongo.db.projects.update_one({"_id": ObjectId(id)}, {"$set": updated_project})
        return redirect(url_for('main.project', id=id))
    return render_template('update_project.html', project=project)

@bp.route('/delete/<id>')
def delete_project(id):
    mongo.db.projects.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('main.index'))
