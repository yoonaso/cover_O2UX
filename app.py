# from os import name
from io import TextIOBase
from os import name
import re
import sqlite3
from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from test import get_grade

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    num = db.Column(db.String(100))
    name = db.Column(db.String(100))
    grade = db.Column(db.String(100))

    def __init__(self, username, password, num, name, grade):
        self.username = username
        self.password = password
        self.num = num
        self.name = name
        self.grade = grade


@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('index.html')
    else:
        # return render_template('index.html', message="로그인성공")
        return render_template('index.html')

@app.route('/grade/', methods=['GET'])
def grade():
    if session.get('logged_in'):
        return render_template('grade.html')
    else:
        # return render_template('index.html', message="로그인성공")
        return render_template('index.html', message="로그인이 필요한 서비스입니다.")

@app.route('/school_login/', methods=['GET', 'POST'])
def school_login():
    if request.method == 'GET':
        return render_template('school_login.html')
    else:
        name = request.form['username']
        password = request.form['password']
        try:
            print("ASDASDAS")
            import test
            global score
            score = test.get_grade(name, password)
            print(score)
            print("ASDASDAS")
            # if score == None :
            #     return render_template('school_login.html', message = 'ID or Password is incorrect')
            # else :
                # return render_template('grade.html', score_list = score)
            return render_template('grade.html', score_list = score)
                # if data is not None:
                #     session['logged_in_school'] = True
                #     return redirect(url_for('index'))
                # else:
                #     return render_template('school_login.html', message='ID or Password is incorrect')
        except Exception as e:
            print(e)
            return render_template('school_login.html', message='ID or Password is incorrect')

@app.route('/result_grade/', methods=['GET', 'POST'])
def result_grade():
    if request.method == 'POST':
        print("ASD")
        test = request.args.get('inter')
        print(test)
        global score
        print(session['name'])
        credit = 0
        for i in score :
            credit += i[3]
        return render_template('grade_complete.html', \
                                grade = session['grade'], \
                                num = session['num'], \
                                name = session['name'], \
                                all_count = credit
                                )
        


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=username, password=password).first()
            if data is not None:
                session['user'] = username
                session['name'] = data.name
                session['num'] = data.num
                session['grade'] = data.grade
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                return render_template('login.html', message='ID or Password is incorrect')
        except:
            return render_template('login.html', message='ID or Password is incorrect')


@app.route('/find_password/', methods=['GET', 'POST'])
def find_password():
    if request.method == 'GET' :
        return render_template('find_password.html')
    else :
        username = request.form['username']
        num = request.form['num']
        name = request.form['name']
        try :
            data = User.query.filter_by(username=username, num=num, name=name).first()
            if data is not None :
                print("Correct")
                import random
                import string
                random_password = "".join([random.choice(string.ascii_uppercase) for _ in range(10)])
                data.password = random_password
                db.session.commit()
                return render_template('new_password.html', message = random_password)
            else :
                return render_template('find_password.html', message = "사용자를 찾을수 없습니다.")
        except :
            return render_template('find_password.html', message = "사용자를 찾을수 없습니다.")

@app.route('/change_information/', methods=['GET', 'POST'])
def change_information():
    if request.method == 'GET' :
        return render_template('change_information.html')
    else :
        # username = request.form['username']
        num = request.form['num']
        grade = request.form['grade']
        name = request.form['name']
        password = request.form['password']
        new_password = request.form['new_password']
        password_confirm = request.form['password_confirm']
        if new_password != password_confirm :
            return render_template('change_information.html', message = "새로운 비밀번호가 다릅니다.")
        data = User.query.filter_by(username=session['user'], password=password).first()
        if data is not None :
            print("Correct Password")
            # data.username = username
            data.num = num
            data.grade = grade  
            data.name = name
            data.password = new_password
            db.session.commit()
            flash("정보수정이 완료되었습니다. \n 처음 화면으로 돌아갑니다.")
            return render_template('change_information.html')  
        else :
            print("Incorrect")
            return render_template('change_information.html', message = "기존 비밀번호를 확인해 주세요.")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new_user = User(username=request.form['username'], password=request.form['password'], num=request.form['num'], name=request.form['name'], grade=request.form['grade'])
            db.session.add(new_user)
            db.session.commit()
            return render_template('register_complete.html', message=request.form['username'])
        except Exception as e:
            print(e)
            return render_template('register.html', message='ID is Exsit')
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.debug = True
    db.create_all()
    app.run(host='0.0.0.0')
