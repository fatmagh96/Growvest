from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.project import Project

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash



bcrypt = Bcrypt(app)

class User:
    def __init__(self, data_dict):
        self.id = data_dict['id']
        self.first_name = data_dict['first_name']
        self.last_name = data_dict['last_name']
        self.email = data_dict['email']
        self.password = data_dict['password']
        self.type = data_dict['type']
        self.wallet = data_dict['wallet']
        self.image = data_dict['image']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        

    # ------ CREATE USER --------

    @classmethod
    def create_user(cls, data_dict):
        query = """
                INSERT INTO users (first_name,last_name,email,password, type, wallet)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(type)s, %(wallet)s);
                """
        # result = connectToMySQL(DATABASE).query_db(query,data_dict)
        return connectToMySQL(DATABASE).query_db(query,data_dict)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(DATABASE).query_db(query)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        return all_users
    
    # get all investors
    
    @classmethod
    def get_all_investors(cls):
        query = "SELECT * FROM users WHERE type = 'investor';"
        result = connectToMySQL(DATABASE).query_db(query)
        all_investors = []
        for row in result:
            all_investors.append(cls(row))
        return all_investors
    ##########################################################
      # get all investors
    @classmethod
    def get_all_investors_investment(cls,all_investors):
        for investor in all_investors:
            investment_investor_query = "SELECT * FROM investments WHERE user_id = {};".format(investor.id)
            investment_result = connectToMySQL(DATABASE).query_db(investment_investor_query)
            invesment_amount = 0
            for row in investment_result:
                invesment_amount += row['amount']
            investor.investment_count= len(investment_result)
            investor.investment_amount=invesment_amount
    ##########################################################
    
    # get all project owners
    
    @classmethod
    def get_all_pos(cls):
        query = "SELECT * FROM users WHERE type = 'po';"
        result = connectToMySQL(DATABASE).query_db(query)
        all_pos = []
        if result:
            for row in result:
                all_pos.append(cls(row))
        return all_pos
    ####################################
    
    @classmethod
    def get_user_by_id(cls,data_dict):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data_dict)
        if result:
            return cls(result[0])
        else:
            return False   
    
    @classmethod
    def get_user_by_email(cls,data_dict):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data_dict)
        # print("**********",result,"***********")
        # if len(result)>0:
        if result:
            return cls(result[0])
        return False
    
    # -------- UPDATE ---------------
    @classmethod
    def update_profile(cls, data_dict):
        query = """
                UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s
                WHERE id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result
    
    @classmethod
    def update_password(cls, data_dict):
        query = """
                UPDATE users SET password = %(new_password)s
                WHERE id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result

    # -------- FAVOURITES ------------

    @classmethod
    def add_to_favourites(cls, data_dict):
        query = """ INSERT INTO favourites (project_id, user_id)
                    VALUES (%(project_id)s, %(user_id)s);
                     """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result
    
    @classmethod
    def remove_from_favourites(cls, data_dict):
        query = """ DELETE FROM favourites
                    WHERE user_id = %(user_id)s AND project_id = %(project_id)s;
                     """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result
    
    @classmethod
    def get_favourite_projects_by_user_id(cls, data_dict):
        query = """ SELECT * FROM projects LEFT JOIN favourites ON project_id = projects.id
                    WHERE favourites.user_id = %(user_id)s;
                    """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        favourite_projects = []
        if result:
            for row in result:
                favourite_projects.append(Project(row))
        return favourite_projects
        
    
    @classmethod
    def get_favourite(cls, data_dict):
        query = """ SELECT * FROM favourites
                    WHERE user_id = %(user_id)s AND project_id = %(project_id)s;
                    """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        
        if result:
            return True
        return False

    # ----- ADMIN -----


    # --- ADD MONEY TO WALLET (investor) ------
    @classmethod
    def update_wallet(cls,data_dict):
        query = """
                    UPDATE users SET wallet = %(wallet)s WHERE id = %(id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data_dict)

    




    # --------- VALIDATION -----------

    @staticmethod
    def change_password_validation(data_dict):
        is_valid = True
        user = User.get_user_by_id(data_dict)
        if not bcrypt.check_password_hash(user.password, data_dict['current_password']):
            flash("current password is wrong!" , "change_password")
            is_valid =False
        elif bcrypt.check_password_hash(user.password, data_dict['new_password']):
            flash("new password must be different from current password!" , "change_password")
            is_valid =False
        elif len(data_dict['new_password'])<8:
            flash("Password must be at least 8 characters", "change_password")
            is_valid = False
        elif data_dict['new_password'] != data_dict['confirm_new_password']:
            flash("Password and Confirm password dont match","change_password")
            is_valid = False
        return is_valid

    @staticmethod
    def login_validation(data_dict):
        is_valid = True
        user = User.get_user_by_email(data_dict)
        if not user:
            flash("Email or Password invalid !!",'login')
            print('Email or Password invalid !!')
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, data_dict['password']):
            flash("Email or Password invalid !!",'login')
            print('Email or Password invalid !!')
            is_valid = False
        return is_valid
    

    @staticmethod
    def validate(data_dict):
        is_valid = True
        if len(data_dict['first_name']) < 2:
            flash("First name too short!","first_name")
            is_valid = False
        if len(data_dict['last_name']) < 2:
            flash("Last name too short!","last_name")
            is_valid = False

        # query = "SELECT * FROM users WHERE email = %(email)s;"
        # result = connectToMySQL(DATABASE).query_db(query,data_dict)
        user = User.get_user_by_email(data_dict)
        
        if not EMAIL_REGEX.match(data_dict['email']):
            flash("Invalid Email!!!",'email')
            is_valid=False
        # if len(result)>0:
        if user:
            flash("Email already taken!!","email")
            is_valid = False

        if len(data_dict['password'])<8:
            flash("Password must be at least 8 characters", "password")
            is_valid = False
        # if not pw_regex.match(data_dict['password']):
        #     flash("Password must be at least 8 characters and contain at least one Uppercase and one number", "password")
        #     is_valid = False
        elif data_dict['password'] != data_dict['confirm_password']:
            flash("Password and Confirm password dont match","password")
            is_valid = False

        return is_valid
    

    @staticmethod
    def validate_edit(data_dict):
        is_valid = True
        if len(data_dict['first_name']) < 2:
            flash("First name too short!","first_name")
            is_valid = False
        if len(data_dict['last_name']) < 2:
            flash("Last name too short!","last_name")
            is_valid = False
        return is_valid