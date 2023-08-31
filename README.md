

# pipenv install flask pymysql flask-bcrypt


Change the DATABASE name in  __init__.py

Dont forget the ; for the queries 🙂

singular fel models w plural fel controllers


Link bootstrap:

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">

**********
Models : {
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


if not EMAIL_REGEX.match(email['email']):
            flash("Invalid Email!!!")
            is_valid=False


}

Controllers : {
from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.++++ import ++++++

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
}


Other useful things : 

{% for message in get_flashed_messages(category_filter=['name']) %}
    <p class="text-danger">{{message}}</p>               <!-- display each message in a paragraph tag -->
{% endfor %}

if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,user)
        # if result != ():
        if len(result)>0:
            flash("Email already Taken !!")
            is_valid = False