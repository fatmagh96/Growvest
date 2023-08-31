from flask import render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.team_model import Team
from flask_app.models.update import Update
from datetime import datetime

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# @app.route('/register/project')
# def register_project():
#     return render_template('project_registration.html')

@app.route('/projects/dashboard/accepted')
def po_dashboard_accepted():
    project = Project.get_project_by_user_id({'user_id':session['id']})
    update = Update.get_by_id_update({'id':project.id})
    teams=Team.get_team_by_project({'project_id':project.id})
    all_updates = Update.get_updates({'project_id':project.id})
    days_left = (project.deadline -datetime.now().date()).days
    average_days_in_month = 30.44
    time_left = {
            'months':int(days_left // average_days_in_month),
            'days':round(days_left % average_days_in_month)
        }
    total = project.amount_raised + project.capital
    percentage_value = float(total)*100 / float(project.goal)
    percentage = round(percentage_value)
    print('PERCENTAGE**************', percentage)
    return render_template('dashboard_po_accepted.html',teams=teams,days_left=days_left,time_left=time_left ,project = project , update=update, all_updates=all_updates, total=total, percentage=percentage )


@app.route('/projects/dashboard/pending')
def po_dashboard_pending():
    project = Project.get_project_by_user_id({'user_id':session['id']})
    return render_template('dashboard_po_Pending.html', project = project)

@app.route('/projects/dashboard/rejected')
def po_dashboard_rejected():
    project = Project.get_project_by_user_id({'user_id':session['id']})
    return render_template('dashboard_po_Rejected.html', project = project)


@app.route('/projects/create', methods=['POST'])
def create_project():
    print('PROJECT REQUEST FORM', request.form)
    print('FILLELEELELLE', request.files['image'])
    user = User.get_user_by_id(session)
    if Project.validate(request.form):
        # data = {
        #     **request.form,
        #     'user_id': user.id
        # }
        pic ="flask_app/static/img/"
        vid="flask_app/static/img/"
        file ="flask_app/static/img/"
        if not request.files['image']:
            flash("image is required", "image")
            return redirect('/register/project')
        else:
            uploaded_file = request.files['image']
            pic = 'flask_app/static/img/' + uploaded_file.filename
            uploaded_file.save(pic)
        if not request.files['video']:
            flash("video is required", "video")
            return redirect('/register/project')
        else:
            uploaded_file = request.files['video']
            vid = 'flask_app/static/img/' + uploaded_file.filename
            uploaded_file.save(vid)
        if not request.files['business_plan']:
            flash("business plan is required", "business_plan")
            file =""
            return redirect('/register/project')
        else:
            uploaded_file = request.files['business_plan']
            file = 'flask_app/static/img/' + uploaded_file.filename
            uploaded_file.save(file)

            data = {    
                **request.form,
                'image': pic,
                'video':vid,
                'business_plan':file,
                'user_id': user.id  
            }
        Project.create_project(data)
        return redirect('/projects/dashboard/pending')
    return redirect('/register/project')


@app.route('/projects/<int:project_id>/show')
def show_project(project_id):
    project = Project.get_project_by_id({'id':project_id})
    days_left = (project.deadline -datetime.now().date()).days
    average_days_in_month = 30.44
    time_left = {
            'months':int(days_left // average_days_in_month),
            'days':round(days_left % average_days_in_month)
        }
    total = project.amount_raised + project.capital
    percentage_value = float(total)*100 / float(project.goal)
    percentage = round(percentage_value, 1)

    user = User.get_user_by_id(session)
    if user:
        is_favourited = User.get_favourite({'user_id':user.id, 'project_id':project_id})
    else:
        is_favourited = False
    all_updates = Update.get_updates({'project_id':project.id})
    teams=Team.get_team_by_project({'project_id':project.id})
    return render_template("one_project_show.html", project = project,is_favourited=is_favourited,all_updates=all_updates, teams = teams ,user=user,total = total , percentage=percentage , time_left=time_left)

@app.route('/projects/edit', methods=['POST'])
def edit_project():
    project = Project.get_project_by_id({'id':request.form['project_id']})
    # if request.form['video'] == "":
    #     data= {
    #         **request.form,
    #         'video': project.video
    #     }
    vid = project.video
    if Project.validate_update(request.form):
        if not request.files['video']:
            vid = project.video
        else:
            uploaded_file = request.files['video']
            vid = 'flask_app/static/img/' + uploaded_file.filename
            uploaded_file.save(vid)
        data= {
            **request.form,
            'video': vid
        }
        Project.update_project_info(data)
        flash("Changes Saved! ", 'edit_proj')
    return redirect("/projects/dashboard/accepted#edit")