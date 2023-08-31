from flask import  request, redirect,flash
from flask_app import app
# from flask_app.models.++++ import ++++++
from flask_app.models.user import User
from flask_app.models.update import Update
from flask_app.models.project import Project
import os

@app.route('/updates/create', methods = ['POST'])
def create_updates():
    pic =""
    if request.files['image']=="":
        pic =""
    else:
        uploaded_file = request.files['image']
        pic = 'flask_app/static/img/' + uploaded_file.filename
        uploaded_file.save(pic)
    data = {    
        **request.form,
        'image': pic  
    }
    update = Update.create_update(data)
    return redirect("/projects/dashboard/accepted#updates")


@app.route('/updates/destroy', methods = ['POST'])
def delete():
    print(request.form)
    Update.delete_update(request.form)
    return redirect('/projects/dashboard/accepted#updates')

# @app.route('/updates_update/<int:update_id>', methods=['POST'])
# def edit_update(update_id):
#     if not Update.validate_update(request.form):
#         id =request.form['id']
#         return redirect(f'/update/edit/{id}')
#     new_image = request.files['image']
#     if new_image:
#             # Save the new image to the server
#             filename = os.path.join(app.config['UPLOAD_FOLDER'], new_image.filename)
#             new_image.save(filename)

#     Update.update_update(request.form)
#     return redirect("/projects/dashboard/accepted#updates")


