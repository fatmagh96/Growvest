from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import app
from flask import flash

from flask_app.models.project import Project
from flask_app.models.user import User


class Investment:
    def __init__(self, data_dict):
        self.id = data_dict['id']
        self.project_id = data_dict['project_id']
        self.user_id = data_dict['user_id']
        self.amount = data_dict['amount']
        self.created_at = data_dict['created_at']
        self.updated_at = data_dict['updated_at']
        self.project = ""

    # ------------- MAKE INVESTMENT --------------

    @classmethod
    def make_investment(cls, data_dict):
        query = """
                    INSERT INTO investments (project_id, user_id, amount)
                    VALUES (%(project_id)s, %(user_id)s, %(amount)s);
                """
        return connectToMySQL(DATABASE).query_db(query, data_dict)
    

    
    @classmethod
    def get_all_projects_invested_in_by_user_id(cls, data_dict):
        query = """
                    SELECT * FROM investments LEFT JOIN projects ON project_id = projects.id
                    WHERE investments.user_id = %(user_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        all_investments = []
        if result:
            for row in result:
                investment = cls(row)
                data = {
                    **row, 
                    'user_id': row['projects.user_id'],
                    'created_at': row['projects.created_at'],
                    'updated_at': row['projects.updated_at']
                }
                investment.project = Project(data)
                all_investments.append(investment)
        return all_investments
        # return False
    
    # @classmethod
    # def get_all_investments_by_user_id(cls, data_dict):
    #     query = """
    #                 SELECT * FROM investments LEFT JOIN projects ON project_id = projects.id
    #                 WHERE user_id = %(user_id)s;
    #             """
    #     result = connectToMySQL(DATABASE).query_db(query, data_dict)
    #     all_investments = []
    #     for row in result:
    #         investment = cls(row)
    #         data = {
    #             **row, 
    #             'user_id': projects.user_id,
    #             'created_at': projects.created_at,
    #             'updated_at': projects.updated_at
    #         }
    #         investment.project = Project(data)
    #         all_investments.append(investment)
    #     return all_investments
    
    @classmethod
    def get_all_investments_by_project_id(cls, data_dict):
        query = """
                    SELECT * FROM investments LEFT JOIN projects ON project_id = projects.id
                    WHERE user_id = %(user_id)s;
                """
        result = connectToMySQL(DATABASE).query_db(query, data_dict)
        all_investments = []
        if result:
            for row in result:
                investment = cls(row)
                investment.project_title = row['title']
                all_investments.append(investment)
        return all_investments

