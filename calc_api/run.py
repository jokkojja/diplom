from fastapi import FastAPI, Body, status
from fastapi.responses import Response
import requests
import uvicorn
import subprocess
from config import CALCULATOR_PATH, PROG_NAME_CPP, PROG_NAME_EXE, service
import os
import psutil
import signal
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

app = FastAPI()
def is_file_on_drive(user_folder_id, filename, service=service):
    query = f"name='{filename}' and parents='{user_folder_id}'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    try:
        id_of_file = [i['id'] for i in items if i['name'] == filename][0]
        return True, id_of_file
    except: 
        return False, ''
    
def delete_file_from_dirve(delete_file_id, service=service):
    try:
        service.files().delete(fileId=delete_file_id).execute()
    except HttpError as error:
        pass
    
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
def upload_results(data = Body()):
    try:
        results_file_path = os.path.join("data", f"concetr_{data['process_id']}.dat")
        if os.path.exists(results_file_path):
            root_folder = service.files().list(q='name = "calculations"', fields="nextPageToken, files(id, name)").execute()
            root_folder_id = root_folder.get('files', [])[0]['id']
            username = data['username']
            result = service.files().list(q = f'name = "{username}" and "{root_folder_id}" in parents', fields="nextPageToken, files(id, name)").execute()
            user_folder_id = result.get('files', [])[0]['id'] 
            file_on_drive, id_of_file = is_file_on_drive(
                user_folder_id=user_folder_id,
                filename=f"concetr_{data['process_id']}.dat")
            if file_on_drive:
                delete_file_from_dirve(
                delete_file_id=id_of_file
                )
            file_metadata = {
                        'name': f"concetr_{data['process_id']}.dat",
                        'mimeType': "application/octet-stream",
                        'parents': [user_folder_id]
                    }              
            file_body = MediaFileUpload(results_file_path, resumable=True, chunksize = 5 * 1024 * 1024)
            request = service.files().create(body=file_metadata, media_body=file_body, fields='id')
            response = None
            try:
                while response is None:
                    _, response = request.next_chunk()  
                return Response(content = response['id'], status_code=status.HTTP_200_OK)
            
            except Exception as e:   
                return Response(content = f"Извините, ошибка во время загрузки файла: {e}", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR)                 
    except Exception as e:
        return Response(content = f"Извините, что-то пошло не так. Ошибка: {e}", status_code = status.HTTP_400_BAD_REQUEST)
        
if __name__ == '__main__':
   uvicorn.run(app, host="127.0.0.1", port=8053)
