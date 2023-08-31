from flask import render_template, request, redirect, session, url_for
from flask_app import app
# from flask_app.models.++++ import ++++++
from flask_app.models.user import User
from flask_app.models.project import Project



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register')
def register_user():
    #template 
    return render_template('registration.html')

@app.route('/register/project')
def register_project():
    return render_template('project_registration.html')


@app.route('/explore')
def explore():
    # projects = Project.get_all_projects()
    projects = Project.get_all_accepted_projects()
    return render_template('all_projects.html', projects= projects)

# @app.route('/projects/id/show')
# def project_show():
#     return render_template('one_project_show.html')


# @app.route('/open-modal')
# def open_modal():
#     return render_template('home.html', open_modal=True)

# @app.route('/redirect-to-modal')
# def redirect_to_modal():
#     # Construct the URL with the query parameter
#     url_with_modal = url_for('open_modal', _external=True) + '?open_modal=true'
#     return redirect(url_with_modal)