from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.team_model import Team 




@app.route('/team_member/create', methods = ['POST'])
def add_team():
    print(request.form)
    uploaded_file = request.files['image']
    pic = 'flask_app/static/img/' + uploaded_file.filename
    uploaded_file.save(pic)
    data = {
        **request.form,
        'image': pic
    }
    print(data)
    Team.create_team(data)
    return redirect("/projects/dashboard/accepted#team")




@app.route('/team/destroy', methods = ['POST'])
def delete_team_member():
    print(request.form)
    Team.delete_team(request.form)
    return redirect("/projects/dashboard/accepted#team")




# @app.route('/team/<int:team_id>/update', methods = ['POST'])
# def update_team(team_id):
#     if Team.validate(request.form):
#         data = {
#             **request.form,
#             'id':team_id
#         }
#         Team.update(data)
#         return redirect('/dashboard')
#     return redirect(f'/team/{team_id}/edit')









