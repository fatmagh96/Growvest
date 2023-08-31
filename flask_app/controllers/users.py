from flask import render_template, request, redirect, session, url_for, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.project import Project

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    user = User.get_user_by_id(session)
    if user.type == 'admin':
        all_projects = Project.get_all_projects()
        project_count = len(all_projects)
        all_investors = User.get_all_investors() 
        User.get_all_investors_investment(all_investors)
        investor_count = len(all_investors) 
        # all_pos = User.get_all_pos()
        all_pos =  Project.get_projects_by_po()
        pos_count = len(all_pos)
        all_pending_projects = Project.get_all_pending_projects()
        all_accepted_projects = Project.get_all_accepted_projects()
        all_declined_projects = Project.get_all_declined_projects()
        admin = User.get_user_by_id({'id':session['id']})
        # all_investments = Investment.get_all_investments_by_investor()
        return render_template(
            "dashboard_admin.html", admin=admin,
            all_projects=all_projects,project_count=project_count,
            all_investors=all_investors,investor_count=investor_count,
            pos_count=pos_count,all_pending_projects=all_pending_projects,
            all_accepted_projects=all_accepted_projects,
            all_declined_projects=all_declined_projects, all_pos=all_pos,
            )
    if user.type == 'investor':
        return redirect('/investors/dashboard')
    if user.type == 'po':
        project = Project.get_project_by_user_id({'user_id':session['id']})
        if project.status == 'pending':
            return redirect('/projects/dashboard/pending')
        if project.status == 'accepted':
            return redirect('/projects/dashboard/accepted')
        if project.status == 'rejected':
            return redirect('/projects/dashboard/rejected')
        

@app.route('/users/create', methods = ['POST'])
def create():
    print('USER REQUEST FORM',request.form,'****************')
    if User.validate(request.form):
        pw_hashed = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hashed)
        data = {
            **request.form,
            'password': pw_hashed
        }
        user_id = User.create_user(data)
        session['id'] = user_id
        if request.form['type'] == 'po':
            return redirect('/register/project')
        return redirect('/dashboard')
        
    return redirect('/register')

@app.route('/signin')
def signin():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    # print(request.form)
    if User.login_validation(request.form):
        user = User.get_user_by_email(request.form)
        print('💲'*5,user.wallet,'💲'*5)
        session['id'] = user.id
        return redirect('/dashboard')
    return redirect('/signin')




