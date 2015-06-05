#!/usr/bin/env python
#-*-coding:utf-8-*-

import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash

#创建app
app = Flask(__name__)
app.config.from_object('config')


#连接数据库
def connect_db():
    row = sqlite3.connect(app.config['DATABASE'])
    row.row_factory = sqlite3.Row
    return row


#定义全局变量g.db
@app.before_request  
def before_request():
    g.db = connect_db()


#初始化数据库
def init_db():
    #创建应用环境
    with app.app_context():
        #获取连接数据库资源
        db = connect_db()
        #读取资源s,在with语句的内部，g对象会与app关联。
        with app.open_resource('schema.sql',mode = 'r') as f:
            #获取游标对象
            db.cursor().executescript(f.read())
        #提交事务
        db.commit()


#显示数据
@app.route('/')
def show_entries():
    #构造sql语句并执行
    cur = g.db.execute('select title,text from entries order by id desc')
    #列表生成式
    entries = [dict(title = row[0],text = row[1]) for row in cur.fetchall()]
    return render_template('showentries.html',entries = entries)


#添加数据
@app.route('/add',methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    #?占位符用于避免sql注入
    g.db.execute('insert into entries(title,text) values(?,?)',[request.form['title'],request.form['text']])
    g.db.commit()
    #消息闪现
    flash('新条目已成功插入数据库!')
    return redirect(url_for('show_entries'))

#登陆
@app.route('/login',methods = ['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        #账号密码合法性检验
        if request.form['username'] != app.config['USERNAME']:
            error = '用户名错误!'
        elif request.form['password'] != app.config['PASSWORD']:
            error = '密码错误!'
        else:
            #通过校验,将session中logged_in置为True
            session['logged_in'] = True
            flash('登陆成功!')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

#注销
@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('注销成功!')
    return redirect(url_for('show_entries'))

