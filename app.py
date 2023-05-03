from flask import Flask, render_template, jsonify, request, session, redirect, url_for,flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

client = MongoClient('localhost',27017)
db = client['SWE']
collection = db['user']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')
        confirm_pw = request.form.get('confirm_pw')

        if collection.find_one({'id':id}):
            flash('이미 존재하는 아이디 입니다.')
            return redirect(url_for('signup'))

        if pw != confirm_pw:
            flash('비밀번호가 일치하지 않습니다.')
            return redirect(url_for(signup))
        
        hashed_pw = generate_password_hash(pw, method='sha256')

        user = {'id':id, 'pw':hashed_pw}
        collection.insert_one(user)
        flash('회원가입에 성공하였습니다!')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        pw = request.form.get('pw')

    if id == '':
        flash("ID를 입력해주세요")
        return render_template("login.html")
    elif pw == '':
        flash("비밀번호를 입력해주세요")
        return render_template("login.html")
    
    user = collection.find_one({'id':id})
    if not user:
        flash('회원정보가 없습니다.')
        return redirect(url_for('login'))
    
    if not check_password_hash(user['pw'],pw):
        flash('아이디와 비밀번호가 일치하지않습니다.')
        return redirect(url_for('login'))
    session['id'] = id
    flash('로그인 성공!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')

@app.route('/main')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)