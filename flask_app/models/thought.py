from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the friend table from our database
class Thought:
    def __init__( self , data ):
        self.id = data['id']
        self.thought = data['thought']
        self.likes = data['likes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def get_all_thoughts(cls):
        query = "SELECT * FROM thoughts JOIN users ON users.id = thoughts.user_id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('thoughts').query_db(query)
        # Create an empty list to append our instances of friends
        thoughts = []
        # Iterate over the db results and create instances of friends with cls.
        for thought in results:
            thoughts.append( cls(thought) )
        return thoughts
    

    @classmethod
    def get_user_thoughts(cls, data):
        query = "SELECT * FROM thoughts WHERE user_id = %(user_id)s;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('thoughts').query_db(query,data)
        thoughts = []
        # Iterate over the db results and create instances of friends with cls.
        for thought in results:
            thoughts.append( cls(thought) )
        return thoughts

    @classmethod
    def save_thought(cls, data ):
        query = "INSERT INTO thoughts ( thought , likes, created_at, updated_at, user_id ) VALUES ( %(thought)s, 0, NOW() , NOW(), %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('thoughts').query_db( query, data )

    @classmethod
    def destroy(cls, data ):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('thoughts').query_db( query, data )

    @classmethod
    def get_one_thought(cls,data):
        query  = "SELECT * FROM thoughts WHERE id = %(id)s;"
        result = connectToMySQL('thoughts').query_db(query,data)
        return cls(result[0])

    @classmethod
    def like(cls,data):
        query = "UPDATE thoughts SET likes = likes + 1 WHERE id = %(id)s;"
        return connectToMySQL('thoughts').query_db(query,data)

    @classmethod
    def dislike(cls,data):
        query = "UPDATE thoughts SET likes = likes - 1 WHERE id = %(id)s;"
        return connectToMySQL('thoughts').query_db(query,data)


    @staticmethod
    def validate_submission(thought):
        is_valid = True # we assume this is true
        if len(thought['thought']) < 5:
            flash("Thought must be 5 characters")
            is_valid = False
        return is_valid
    
class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.comment = data['comment']
        self.thought_id = data['thought_id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_comments(cls,data):
        query  = "SELECT * FROM comments WHERE thought_id = %(id)s;"
        results = connectToMySQL('thoughts').query_db(query, data)
        # Create an empty list to append our instances of friends
        comments = []
        # Iterate over the db results and create instances of friends with cls.
        for comment in results:
            comments.append( cls(comment) )
        return comments

    @classmethod
    def save_comment(cls, data ):
        query = "INSERT INTO comments ( comment , thought_id, user_id, created_at, updated_at ) VALUES ( %(comment)s, %(id)s, %(user_id)s, NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('thoughts').query_db( query, data )

    @classmethod
    def destroy_comment(cls, data ):
        query = "DELETE FROM comments WHERE id = %(comment_id)s;"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('thoughts').query_db( query, data )

