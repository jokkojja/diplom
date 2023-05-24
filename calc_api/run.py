from fastapi import FastAPI, Body, status
from fastapi.responses import Response
import requests
import uvicorn
import subprocess
from config import CALCULATOR_PATH, PROG_NAME_CPP, PROG_NAME_EXE
import os
import psutil
import signal

app = FastAPI()

@app.post('/calc')
def calc(data = Body()):

    try:
        username = data['username']
        calc_id = data['calc_id']
        data.pop('username')
        subprocess.run([f'g++ -o ../{os.path.join(CALCULATOR_PATH, PROG_NAME_EXE + "_" + username + "_" + calc_id)} ../{os.path.join(CALCULATOR_PATH, PROG_NAME_CPP)}'], shell=True)
        cmd = f'../{os.path.join(CALCULATOR_PATH, PROG_NAME_EXE + "_" + username + "_" + calc_id + " ")}'
        for i in data.values():
            cmd += str(i) + ' '
        process = subprocess.Popen([cmd], shell=True)
        return Response(content = str(process.pid), status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)
    
@app.get('/calc_status/{process_pid}')
def get_status(process_pid):
    try:
        is_process_active = psutil.pid_exists(int(process_pid))
        process_status = 'Active' if is_process_active is True else 'Inactive'
        return Response(content = process_status, status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)

@app.post('/stop_calculate')
def stop_calculate(data = Body()):
    try:
        pid = data['pid']
        is_process_active = requests.get(url=f"http://127.0.0.1:8053/calc_status/{pid}").content.decode('utf-8')
        if is_process_active == 'Active':
            os.kill(int(pid), signal.SIGKILL)
            try:
                os.remove(f'../calculating_waves/progr_{data["username"]}_{data["process_id"]}')
            except FileNotFoundError:
                pass  
            return Response(content = "Процесс был остановлен", status_code=status.HTTP_200_OK)
        else:
            return Response(content = "Нет такого активного процесса", status_code=status.HTTP_200_OK)
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)

@app.post('/upload_results')
def upload_results():
    pass
if __name__ == '__main__':
   uvicorn.run(app, host="127.0.0.1", port=8053)
