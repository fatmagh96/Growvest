from flask import render_template, request, redirect, session, flash, url_for
from flask_app import app

from flask_app.models.user import User
from flask_app.models.project import Project
from flask_app.models.investment import Investment

# /investments/new/{{project.id}}
@app.route('/investments/new/<int:project_id>', methods=['POST'])
def make_investments(project_id):
    print('MAKE INVESTMENT REQUEST FORM ', request.form)
    user = User.get_user_by_id({'id':request.form['user_id']})
    if float(request.form['amount']) <= float(user.wallet):
        print("***************** TRUE ****************")
        data = {
            **request.form,
            'project_id':project_id
        }
        Investment.make_investment(data)
        data_project = {
            'amount_raised': request.form['amount'] ,
            'project_id': project_id
        }
        Project.updated_amount_raised(data_project)
        amount =  float(user.wallet) - float(request.form['amount'])
        data_wallet = {
            'wallet' : amount,
            'id' : session['id']
        }
        User.update_wallet(data_wallet)
        flash("Successful Transaction!" , "investment_success")
        return redirect(url_for('show_project',project_id=project_id))
    flash("Insufficient funds in Wallet", "investment_danger")
    print(print("***************** FALSE ****************"))
    # return redirect(f"/projects/{project_id}/show")
    return redirect(url_for('show_project',project_id=project_id))
