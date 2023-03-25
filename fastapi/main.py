import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
import json
import requests
 
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.id = str(uuid.uuid4())
 
people = [Person("Tom", 38), Person("Bob", 42), Person("Sam", 28)]

def find_person(id):
   for person in people: 
        if person.id == id:
           return person
   return None
 
app = FastAPI()


@app.get("/")
async def main():
    
    return FileResponse("public/index.html")
 
@app.get("/api/users")
def get_people():
    return people
 
@app.get("/api/users/{id}")
def get_person(id):
    person = find_person(id)
    print(person)
    if person==None:  
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Пользователь не найден" }
        )
    return person
 
 
@app.post("/api/users")
def create_person(data  = Body()):
    #data["age"] = requ(data["age"],5)-----------------------connect with Flask and post request
    person = Person(data["name"], data["age"])
    people.append(person)
    return person
 
@app.put("/api/users")
def edit_person(data  = Body()):
  
    # получаем пользователя по id
    person = find_person(data["id"])
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None: 
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Пользователь не найден" }
        )
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    person.age = data["age"]
    person.name = data["name"]
    return person
 
 
@app.delete("/api/users/{id}")
def delete_person(id):
    # получаем пользователя по id
    person = find_person(id)
  
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "message": "Пользователь не найден" }
        )
  
    # если пользователь найден, удаляем его
    people.remove(person)
    return person

def requ(one, two):
    req = requests.get("http://127.0.0.1:5000/")
    print(req.status_code)
    js = {}
    js['first'] = one
    js['two'] = two
    req = requests.post(url = "http://127.0.0.1:5000/calc",json = js)
    req = req.json()
    return req['response']