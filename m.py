from flask import Flask, render_template, jsonify, request, session, redirect, url_for,flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey' 
client = MongoClient("mongodb://localhost",27017)
db = client.SWE
collection = db.user
user = {'id':"minseo",
        "pw":'123'}
collection.insert_one(user)
user = {'id':"min",
        "pw":'1234'}
collection.insert_one(user)

result = collection.find()
for r in result:
    print(r)