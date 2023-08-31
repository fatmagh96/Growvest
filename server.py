from flask_app import app
from flask import render_template, redirect

# ! DONT FORGET TO IMPORT CONTROLLERS

from flask_app.controllers import visitors, investors, admin_controller, users, projects, investments, updates, team_controller



if __name__ =="__main__":
    app.run(debug=True, port=5001)
