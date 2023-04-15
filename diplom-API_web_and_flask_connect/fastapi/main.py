from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response
import requests
import uvicorn
import sys
sys.path.insert(1, '../')
from utils.work_with_database import check_username, check_user_password
 
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
        if check_username(data['login']) and check_user_password(data['pass']):
            return True
        else:
            return False
    except Exception:
        return Response(content = "Sorry, something went wrong\n", media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8052)