import requests
from utils.config import LOGIN_PATH, REG_PATH, CALC_PATH, HISTORY_PATH, STOP_CALC_PATH, DOWNLOAD_PATH

class UserFinctionality:
    def __init__(self):
        self.__login_path = LOGIN_PATH
        self.__register_path = REG_PATH
        self.__calculate_path = CALC_PATH
        self.__history_path = HISTORY_PATH
        self.__stop_calc_path = STOP_CALC_PATH
        self.__download_path = DOWNLOAD_PATH
    
    def send_register(self, username, password, email):
        response = requests.post(url=self.__register_path, 
                      json={
                          'username': username,
                          'password': password,
                          'email': email
                          })
        return response

    def send_login(self, username, password):
        response = requests.post(url=self.__login_path, 
                      json={
                          'username': username,
                          'password': password,
                          })
        return response        
    
    def send_calculate(self, json):
        response = requests.post(
                    url=self.__calculate_path, 
                    json=json
                    )
        return response 
    
    def send_history(self, username):
        response = requests.post(url=self.__history_path, 
                      json={
                          'username': username,
                          })
        return response     
    
    def send_stop_calculate(self, data):
        response = requests.post(url=self.__stop_calc_path, 
                                 json=data)   
        return response 
    
    def send_download(self, data):
        response = requests.post(url=self.__download_path, 
                                 json=data)   
        return response         