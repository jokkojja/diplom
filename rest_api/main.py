from fastapi import FastAPI, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
import requests
import uvicorn
from utils.user import User
import uuid
import json
 
app = FastAPI()

@app.post("/api/calc")
async def start_calculate(data = Body()):
    try:
        user = User(data)
        calc_id = str(uuid.uuid4())
        data['calc_id'] = calc_id
        res = requests.post(url='http://127.0.0.1:8053/calc', json=data) #отправка данных расчета на сервер вычислений
        if res.status_code == 200:
            data['process_pid'] = res.content.decode('utf-8')
            await user.add_calculation_data(data)
            return Response(content = 'Расчет успешно запущен', status_code=200)
    except Exception:
        return Response(content = 'Failure: invalid JSON!\n', media_type="text/plain", status_code=500)
    
@app.post("/api/login")
async def login(data = Body()):
    try:
        user = User(data)
        if not await user.is_user_exist():
            return Response(content = "Пользователя с таким логином не существует", status_code=status.HTTP_401_UNAUTHORIZED)
        
        elif not await user.check_user_password():
            return Response(content = "Неверный пароль", status_code=status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response(content = "Авторизация успешна", status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)

@app.post("/api/reg")
async def registration(data = Body()):
    try:
        user = User(data)
        if not await user.is_user_exist():
            user_id = await user.create_user()
            folder_id = await user.create_user_folder()
            return Response(content = f"Пользователь создан с ID: {user_id}. ID папки: {folder_id}", status_code = status.HTTP_200_OK)
        else:
            return Response(content = "Такой логин уже используется", status_code = status.HTTP_409_CONFLICT)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)
    
@app.post("/api/history")
async def history(data = Body()):
    try:
        user = User(data)
        calculations = await user.get_calculating_history()
        return JSONResponse(content = jsonable_encoder(calculations), status_code = status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)
    
@app.post("/api/stop_calculation")
def stop_calculate(data = Body()):
    try:
        user = User(data)
        res = requests.post(url='http://127.0.0.1:8052/api/calculation_pid', json=data)
        res = requests.post(url='http://127.0.0.1:8053/stop_calculate', json=res.json())
        if res.status_code == 200:
            user.update_process_status(data['process_id'])
        return Response(content = res.content.decode('utf-8'), status_code = status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)

@app.post("/api/calculation_pid")
async def get_pid(data = Body()):
    try:
        process_id = data['process_id']
        user = User(data)
        data = await user.get_pid(process_id)
        data['process_id'] = process_id
        data['username'] = user.username
        return JSONResponse(content = jsonable_encoder(data), status_code = status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)
 
@app.post("/api/download")       
def download(data = Body()):
    try:
        res = requests.post(url='http://127.0.0.1:8052/api/upload_results', json=data)
        
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)        
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8052)
