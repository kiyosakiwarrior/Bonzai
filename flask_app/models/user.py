# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# model the class after the friend table from our database
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('thoughts').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('thoughts').query_db( query, data )

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('thoughts').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_one_by_id(cls,data):
        query  = "SELECT * FROM users WHERE id = %(user_id)s;"
        result = connectToMySQL('thoughts').query_db(query,data)
        print(result)
        return cls(result[0])


    @staticmethod
    def unique_email( user ):
        is_valid = True
        query = "SELECT email FROM users;"
        results = connectToMySQL('thoughts').query_db(query)
        for email in results:
            if email['email'] == user['email']:
                flash("This email is already taken.")
                is_valid = False
                return is_valid
        return is_valid

    @staticmethod
    def validate_email( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid

    @staticmethod
    def email_match( user ):
        is_valid = False
        query = "SELECT email FROM users;"
        results = connectToMySQL('thoughts').query_db(query)
        for email in results:
            if email['email'] == user['email']:
                is_valid = True
                return is_valid
        flash("That is not a valid email address")
        return is_valid

    @staticmethod
    def password_match( user ):
        is_valid = False
        query = "SELECT password FROM users;"
        results = connectToMySQL('thoughts').query_db(query)
        for password in results:
            if password['password'] == user['password']:
                is_valid = True
                return is_valid
        flash("That is not a valid password")
        return is_valid

    @staticmethod
    def validate_registration(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 2:
            flash("Name must be greater than 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be greater than 2 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be 8 characters")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Password must match Confirm Password.", "password")
            is_valid = False
        return is_valid

