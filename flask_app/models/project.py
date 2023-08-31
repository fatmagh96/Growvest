from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from datetime import datetime
from datetime import timedelta

class Project:
    def __init__(self,data_dict):
        self.id = data_dict['id']
        self.user_id = data_dict['user_id']
        self.title = data_dict['title']
        self.model = data_dict['model']
        self.category = data_dict['category']
        self.description = data_dict['description']
        self.pitch = data_dict['pitch']
        self.status = data_dict['status']
        self.capital = data_dict['capital']
        self.goal = data_dict['goal']
        self.amount_raised = data_dict['amount_raised']
        self.total = float(data_dict['amount_raised']) + float(data_dict['capital'])
        self.percentage = round(float(self.total)*100 / float(data_dict['goal']),1)
        self.deadline = data_dict['deadline']
        self.tax_code = data_dict['tax_code']
        self.bank_details = data_dict['bank_details']
        self.acceptance_date = data_dict['acceptance_date']
        self.image = data_dict['image']
        self.video = data_dict['video']
        self.business_plan = data_dict['business_plan']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        self.investors = []
        self.po = ''

    #======================CREATE==========================

    @classmethod
    def create_project(cls, data_dict):
        query = """
                INSERT INTO projects (user_id, title, model,category,description,pitch,status,capital,goal,amount_raised,deadline,
                tax_code,bank_details,business_plan,image,video) 
                VALUES (%(user_id)s,%(title)s,%(model)s,%(category)s,%(description)s,%(pitch)s,%(status)s,%(capital)s,%(goal)s,%(amount_raised)s,%(deadline)s,
                %(tax_code)s,%(bank_details)s,%(business_plan)s,%(image)s,
                %(video)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data_dict)
    
    # ---------------------- UPDATE AMOUNT RAISED-----------------

    @classmethod
    def updated_amount_raised(cls, data_dict):
        query = """
                    UPDATE projects SET amount_raised = %(amount_raised)s
                    WHERE id = %(project_id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data_dict)
    
    # --------------- GET PROJECT BY USER ID ----------------
    @classmethod
    def get_project_by_user_id(cls, data_dict):
        query = """
                    SELECT * FROM projects WHERE user_id = %(user_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        if result:
            return cls(result[0])
        return False
    
    # --------------- GET PROJECT BY ID ----------------
    @classmethod
    def get_project_by_id(cls, data_dict):
        query = """
                    SELECT * FROM projects WHERE id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        if result:
            return cls(result[0])
        return False
    
    # ------- GET ALL PROJECTS -----------------
    @classmethod
    def get_all_projects(cls):
        query = "SELECT * FROM projects;"
        result = connectToMySQL(DATABASE).query_db(query)
        all_projects = []
        if result:
            for row in result:
                project = cls(row)
                all_projects.append(project)
        return all_projects
    

    # =================================
    @classmethod
    def get_projects_by_po(cls):
        query = """
                SELECT * FROM projects JOIN users ON projects.user_id = users.id;
                """
        result = connectToMySQL(DATABASE).query_db(query)
        projects = []
        if result:
            for row in result:
                project = cls(row)
                project.po = f"{row['first_name']} {row['last_name']}"
                projects.append(project)
        return projects
    
    # ------- GET ALL Pending PROJECTS -----------------
    @classmethod
    def get_all_pending_projects(cls):
        query = "SELECT * FROM projects where status = 'pending' ORDER BY id desc;"
        result = connectToMySQL(DATABASE).query_db(query)
        pending_projects = []
        if result:
            for row in result:
                project = cls(row)
                pending_projects.append(project)
        return pending_projects
    
    
    
    # ------- GET ALL ACCEPTED PROJECTS -----------------
    @classmethod
    def get_all_accepted_projects(cls):
        query = "SELECT * FROM projects where status = 'accepted' ORDER BY id desc;"
        result = connectToMySQL(DATABASE).query_db(query)
        accepted_projects = []
        if result:
            for row in result:
                project = cls(row)
                accepted_projects.append(project)
        return accepted_projects
    
    # ------- GET ALL declined PROJECTS -----------------
    @classmethod
    def get_all_declined_projects(cls):
        query = "SELECT * FROM projects where status = 'rejected' ORDER BY id desc;"
        result = connectToMySQL(DATABASE).query_db(query)
        declined_projects = []
        if result:
            for row in result:
                project = cls(row)
                declined_projects.append(project)
        return declined_projects



    # -------- UPDATE status to accepted---------------
    @classmethod
    def pending_to_accepted(cls, data_dict):
        query = """
                UPDATE projects SET status = 'accepted',
                acceptance_date = now()
                WHERE id = %(id)s;
                """
        
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result
    # -------- UPDATE status to decline---------------
    @classmethod
    def decline(cls, data_dict):
        query = """
                UPDATE projects SET status = 'rejected'
                WHERE id = %(id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        return result
    
    # ------------ UPDATE PROJECT INFO ------------------
    @classmethod
    def update_project_info(cls, data_dict):
        query="""UPDATE projects SET video= %(video)s , description = %(description)s , pitch= %(pitch)s
                    WHERE id = %(project_id)s;
                """
        return connectToMySQL(DATABASE).query_db(query, data_dict)

    # ----- validation for update ------
    @staticmethod
    def validate_update(data_dict):
        is_valid = True

        if len(data_dict["description"])<10:
            is_valid = False
            flash("Description too short","description")
        if len(data_dict['pitch'])<10:
            is_valid =False
            flash("Pitch not valid", "pitch")    
        # if data_dict['video'] =='':
        #     is_valid = False
        #     flash("Video is required", "video")
        
        return is_valid







    # ======================VALIDATION =============================
    @staticmethod
    def validate(data_dict):
        is_valid = True
        if len(data_dict['title'])<2:
            is_valid =False
            flash("Title not valid", "title")
        if 'model' not in data_dict or data_dict['model'] not in {
            "b2b", "b2c"
            }:
            is_valid = False
            flash("model is required", "model")
        if len(data_dict["description"])<10:
            is_valid = False
            flash("Description too short","description")
        if len(data_dict['pitch'])<10:
            is_valid =False
            flash("Pitch not valid", "pitch")    
        # if data_dict['image'] =='':
        #     is_valid = False
        #     flash("image is required", "image")

        # if data_dict['video'] =='':
        #     is_valid = False
        #     flash("Video is required", "video")
        
        if 'category' not in data_dict or data_dict['category'] not in {
            "technology", "engineering", "business", 
            "healthcare", "education", "art", 
            "social", "research", "design", 
            "travel", "green-projects", "development", 
            "entertainment"
            }:
            is_valid = False
            flash("Invalid category selection", "category")


        if data_dict['capital']=="":
            is_valid = False
            flash("Cannot be empty", "capital")
        elif int(data_dict['capital'])< 0 :
            is_valid = False
            flash("Amount not valid", "capital")
        
        if data_dict['goal']=="":
            is_valid = False
            flash("Cannot be empty", "goal")
        elif int(data_dict['goal'])< 0 :
            is_valid = False
            flash("Amount not valid", "goal")
        

        max_future_date = datetime.now() + timedelta(days=5 * 365) 
        # date_obj = datetime.strptime( data_dict['deadline'], '%Y-%m-%d')

        if not data_dict['deadline']:
            is_valid = False
            flash("Date is required", "deadline")
        elif datetime.strptime( data_dict['deadline'], '%Y-%m-%d') < datetime.now():
            is_valid = False
            flash("Date should start from today", "deadline")
        elif datetime.strptime( data_dict['deadline'], '%Y-%m-%d') > max_future_date:
            is_valid = False
            flash("Date cannot be superior to 5 years from now", "deadline")
        
        if len(data_dict['tax_code'])<7:
            is_valid =False
            flash("Tax code not valid", "tax_code")

        if len(data_dict['bank_details'])<7:
            is_valid =False
            flash("Bank details not valid", "bank_details")

        
        # if data_dict['business_plan'] =='':
        #     is_valid = False
        #     flash("business plan file is required", "business_plan")

        # if not data_dict.get('terms'):
        #     is_valid = False
        #     flash("You must agree to the terms.", "terms")
        
        return is_valid