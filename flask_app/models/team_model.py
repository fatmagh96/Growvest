from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

#*********************** constructor******************

class Team():
    def __init__(self,data):
        self.id = data['id']
        self.project_id = data['project_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.role = data['role']
        self.summary = data['summary']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



#*********************CRUD Queries**********************

    @classmethod
    def create_team(cls,data):
        query="""INSERT INTO team_members (project_id,first_name,last_name,role,summary,image) 
        VALUES (%(project_id)s,%(first_name)s,%(last_name)s,%(role)s,%(summary)s,%(image)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #!---------------get all team---------------
    @classmethod
    def get_team(cls):
        query="SELECT * FROM team_members;"
        results= connectToMySQL(DATABASE).query_db(query)
        team=[]
        if results:
            for row in results:
                team.append(cls(row))
        return team
    
    # ------------ GET TEAM BY PROJECT ------
    @classmethod
    def get_team_by_project(cls,data):
        query="SELECT * FROM team_members WHERE project_id = %(project_id)s;"

        results= connectToMySQL(DATABASE).query_db(query, data)
        #organize the results
        team=[]
        if results:
            for row in results:
                team.append(cls(row))
        return team
    
    #!-----------------get one teammate by project_id---------
    @classmethod
    def get_team_member_by_id(cls,data):
        query="SELECT * FROM team_members WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    # !------------------update------------------------------
    @classmethod
    def update_team(cls,data):
        query="""UPDATE team_members SET 
        first_name=%(first_name)s,last_name=%(last_name)s,role=%(role)s,summary=%(summary)s,image=%(image)s 
        WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    # !--------------------- Delete team---------------------
    @classmethod
    def delete_team(cls,data):
        query="""DELETE FROM team_members WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)


