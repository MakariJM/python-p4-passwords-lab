#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
        session.pop('page_views', None)
        session.pop('user_id', None)
        return {}, 204

class Signup(Resource):
    
    def post(self):
        json_data = request.get_json()
        user = User(username=json_data['username'])
        user.password_hash = json_data['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):
    
    def get(self):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        if user:
            return user.to_dict()
        else:
            return {}, 204

class Login(Resource):
    
    def post(self):
        data = request.get_json()
        username = data['username']
        user = User.query.filter(User.username == username).first()
        
        if not user:
            return {"error": "Invalid username"}, 401
        
        password = data['password']
        
        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict()
        
        return {"error": "Incorrect password"}, 401  

class Logout(Resource):
    
    def delete(self):
        session.clear()
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

