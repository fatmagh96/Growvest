from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import DATABASE
#******* constructor*************
class Update():
    def __init__(self,data):
        self.id = data['id']
        self.project_id = data['project_id']
        self.title = data['title']
        self.description = data['description']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        #self.owner= None


    #**********CRUD Queries**********

    @classmethod
    def create_update(cls,data):
        query="""INSERT INTO updates (project_id,title,description,image) 
        VALUES (%(project_id)s,%(title)s,%(description)s,%(image)s);"""
        # this query will return the id of the new update insert
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #get all updates
    @classmethod
    def get_updates(cls,data):
        query="SELECT * FROM updates WHERE project_id = %(project_id)s ORDER BY id desc;"

        results= connectToMySQL(DATABASE).query_db(query, data)
        #organize the results
        updates=[]
        if results:
            for row in results:
                updates.append(cls(row))
        return updates
    
    #get one update by id
    @classmethod
    def get_by_id_update(cls,data):
        query="SELECT * FROM updates WHERE id=%(id)s;"
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    @classmethod
    def updates_update(cls,data):
        query="""UPDATE updates SET 
        title=%(title)s,description=%(description)s,image=%(image)s 
        WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def delete_update(cls,data):
        query="DELETE FROM updates WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    




#validate update
    @staticmethod
    def validate_update(data):
        is_valid = True
        if len(data['title'])<1:
            flash("you must add a title","title")
            is_valid = False
        if len(data['description'])<3:
            flash("All fields required","description")
            is_valid = False    
        if not data.get('image'):  # Assuming 'image' is a required field
            flash("Image is required", "image")
            is_valid = False      
        return is_valid