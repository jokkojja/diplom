from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response
import requests
import uvicorn
import sys
sys.path.insert(1, '../')
from utils.work_with_database import check_username, check_user_password,create_user
 
app = FastAPI()

@app.post("/calc")
def calc(data = Body()):
    try:
        res = requests.post(url='http://127.0.0.1:8051/calc', json=data) #отправка данных расчета на сервер вычислений
        return res.status_code
    except Exception:
        return Response(content = 'Failure: invalid JSON!\n', media_type="text/plain", status_code=500)
    
@app.post("/login")
def login(data = Body()):
    try:
        if check_username(data['login']) and check_user_password(data['login'],data['pass']):
            return True
        else:
            return False
    except Exception:
        return Response(content = "Sorry, something went wrong\n", media_type="text/plain")

@app.post("/reg")
def registration(data = Body()):
    try:
        if not check_username(data['login']):
            create_user(data['login'],data['password'],data['email'])
            return True
        else:
            return "Login is already in use"
    except Exception:
        return "Sorry, something went wrong"
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8052)