from dataclasses import dataclass
from typing import Optional, List
from fastapi import Request, Body
from utils.config import mydb, method, service
import re
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import uuid

class User:
    def __init__(self, data: Body):
        self.error: List = [] 
        self.username: Optional[str] = data.get('username')
        self.password: Optional[str] = data.get('password')
        self.email: Optional[str] = data.get('email')     
        
    def __repr__(self):
        return f"User data: {self.username}, {self.password}, {self.email}"
    
    async def is_user_exist(self):
        """ Check username in database.
        Args:
            username (str): Username of user.
        Returns: bool.
        """
        if len(list(mydb.users.find({"username": self.username}))) == 0:
            return False
        else:
            return True 
        
    async def create_user(self) -> str:
        """ Add user to database. Create user folder on google drive.
        Args:
            username (str): Username of user.
            password (str): Password of user.
            email (str): email of user.
            method (str): Encryption method.
        """
        
        encoded_password = self.password_encoding(self.password, method)
        user_id = mydb.users.insert_one({
            "username": self.username,
            "password": encoded_password,
            "email": self.email,
            "calculatingHistory": []
        }).inserted_id
        return user_id
    
    @staticmethod
    def password_encoding(password: str, method: str) -> str:
        hashed_password = generate_password_hash(password, method=method)[len(method):]
        return hashed_password

    @staticmethod
    def check_password(password: str, encoded_password: str, method: str) -> bool:
        return check_password_hash(method + encoded_password, password)
    
    async def check_user_password(self, method: str = method) -> bool:
        """ Check username password.
        Args:
            username (str): Username of user.
            password: (str): Password.
        Returns: bool.
        """
        encoded_password = await self.get_password_from_database()
        return self.check_password(self.password, encoded_password, method)
    
    async def get_password_from_database(self) -> str:
        """ Get username password from database
        Args:
            username (str): Username of user.
        Returns:
            str: encoded password.
        """
        return list(mydb.users.find({"username": self.username}))[0]['password']
    
    async def add_calculation_data(self, data):
        process_pid = data['process_pid']
        calc_id = data['calc_id']
        data.pop('process_pid')
        data.pop('username')
        data.pop('calc_id')
        result_data = mydb.users.update_one({
            "username": self.username
        },
            {
                "$push": {"calculatingHistory":
                    {
                        "datetime": datetime.datetime.now(),
                        "process_pid": process_pid,
                        "calc_id": calc_id,
                        "status": "active",
                        "parameters": data
                    }
                }
            }).raw_result  
        
        return result_data
    
    async def get_calculating_history(self):
        calcs = mydb.users.find(
            {
                "username": self.username
            },
            {
                '_id': 0,
                'calculatingHistory': 1
            }
        )      
        return list(calcs)
    
    async def get_pid(self, process_id):
        try:
            pid = mydb.users.find({
                'username': self.username,
                'calculatingHistory.calc_id': process_id
            }, 
                {
                    '_id': 0,
                    'calculatingHistory': {"$elemMatch": {"calc_id": process_id}},
                    'calculatingHistory.process_pid': 1
                })   
            pid = list(pid)[0]['calculatingHistory'][0]['process_pid']
        except IndexError:
            pid = ''
    
        return {'pid': pid}
    
    def update_process_status(self, process_id):
        result_data = mydb.users.update_one({
            "username": self.username,
            'calculatingHistory.calc_id': process_id
        },
            {
                "$set": {"calculatingHistory.$.status": "stopped"}
                    
                }
            ).raw_result   
        return result_data
    
    async def create_user_folder(self, service=service):
        root_folder = service.files().list(q='name = "calculations"', fields="nextPageToken, files(id, name)").execute()
        root_folder_id = root_folder.get('files', [])[0]['id']
        file_metadata = {
            'name': self.username,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [root_folder_id]
        }

        file = service.files().create(body=file_metadata, fields='id'
                                    ).execute()

        return file['id']  
    
          
