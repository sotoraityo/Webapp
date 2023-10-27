from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import time
import pandas as pd
from sqlalchemy.dialects import postgresql as pg
import os
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash

"""
from main import app, db
with app.app_context():
  db.create_all()
"""

#flaskクラスのインスタンス作成
app = Flask(__name__)
#データベースの作成
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///postdata.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#アカウントのDB
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),nullable=False,unique=True)
    password=db.Column(db.String(25))
#投稿内容のDB
class Post(db.Model):
    #__tablename__ = 'posts'
    #それぞれの項目の設定
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20), nullable=True)
    health=db.Column(db.String(20), nullable=True)
    weight=db.Column(db.Integer,nullable=True)
    breakf = db.Column(db.String(20), nullable=True)
    lunch = db.Column(db.String(20), nullable=True)
    dinner = db.Column(db.String(20), nullable=True)
    detail = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.DateTime, nullable=True)
    #passward=db.Column(db.String(20),nullable=False)
    thred = db.Column(db.Integer, nullable=False)

#
#メインページ
#
@app.route('/', methods=['GET', 'POST'])
#@login_required
def index():
    #Getが来たらindex.htmlのページに飛ぶ
    if request.method=='GET':
        #Postデータベースからすべての投稿を取り出す
        #posts=Post.query.all()
        posts=Post.query.filter(Post.thred==0)
        
        return render_template('index.html', posts=posts)

    #Postのデータを読み取り、postdataにデータを保存し、newpostを作る
    else:
        #フォームからデータの入力、仮の初期値
        user = request.form.get('user',"nanasi")
        health=request.form.get('health',"good")
        weight=request.form.get('weight',"00")
        breakf = request.form.get('breakf',"今日の朝食")
        lunch=request.form.get('lunch',"今日の朝食")
        dinner=request.form.get('dinner',"今日の朝食")
        detail = request.form.get('detail',"ヤマザキパン")
        post_date = request.form.get("post_date","2021-12-31")
        dt_now = datetime.now()
        #passward=request.form.get("passward","0000")
        thred=0

        #文字列から日付型に変換(date)
        post_date = datetime.strptime(post_date, "%Y-%m-%d")
        #dt_now=time.strftime('%Y/%m/%d %H:%M:%S')

        new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                        health=health,weight=weight,
                        detail=detail,post_date=post_date,thred=thred)
        
        db.session.add(new_post)
        db.session.commit()
        return redirect('/calendar')

#
#新規登録サインアップページ
#
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    #***post
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        #username = username.encode('utf-8')
        #password = password.encode('utf-8')
        # Userのインスタンスを作成（セキュリティのためハッシュ化する）
        user = User(username=username, password=generate_password_hash(password, method='sha256'))
        #user = User(username=username, password=password)
        
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

#
#ログインページ
#
@app.route('/login', methods=['GET', 'POST'])
def login():
    #**Post
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

#
#ログアウトページ
#
@app.route('/logout')
#@login_required
def logout():
    #ユーザーをログアウトさせる」
    logout_user()
    return redirect('/login')

#
#投稿作成ページ
#
@app.route('/create', methods=['GET', 'POST'])
#@login_required
def create():
    if request.method=="POST":
        #データを取得、date型に変換する
        select_date=request.form.get('select_date')
        select_date= datetime.strptime(select_date, "%Y-%m-%d")
        #Noneなら今日の日付を返す
        if select_date==None:
            select_date=datetime.now()
        
        return render_template('create.html',datenow=select_date)
    else:
        dt_now =datetime.now()
        return render_template('create.html',datenow=dt_now)

    

#
#詳細ページ　データベースのIDからデータを指定
#
@app.route('/detail/<int:id>')
def detail(id):
    #idの指定
    post = Post.query.get(id)
    comments=Post.query.filter(Post.thred==id)
    dt_now =datetime.now()
    return render_template('detail.html', post=post,comments=comments,datenow=dt_now)
"""""
#
#パスワードページ
#
@app.route('/passcheck/<int:id>',methods=['GET', 'POST'])
def passcheck(id):
    post = Post.query.get(id)
    if request.method=='GET':
        return render_template('passcheck.html', post=post,equal=1)
    else:
        return render_template('passcheck.html', post=post,equal=0)

#
#編集ページ
#
@app.route('/arrange/<int:id>',methods=['GET', 'POST'])
#@login_required
def arrange(id):
    post = Post.query.get(id)
    Inpassward = request.form.get("passward")
    if(post.passward==Inpassward):
        return render_template('arrange.html', post=post, passlength=0)
    else:
        return redirect('/passcheck/'+str(id))
"""
@app.route('/arrange/<int:id>',methods=['GET', 'POST'])
#@login_required
def arrange(id):
    post = Post.query.get(id)
    return render_template('arrange.html', post=post)
    
    
#
#削除ページ
#
@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/calendar')
        

#
#コメントページ
#
@app.route('/comment/<int:id>',methods=['GET', 'POST'])
def comment(id):
    user = request.form.get('user',"nanasi")
    health=request.form.get('health',"good")
    weight=request.form.get('weight',"00")
    breakf = request.form.get('breakf',"今日の朝食")
    lunch=request.form.get('lunch',"今日の朝食")
    dinner=request.form.get('dinner',"今日の朝食")
    detail = request.form.get('detail',"ヤマザキパン")
    post_date = request.form.get("post_date","2021-12-31")
    dt_now = datetime.now()

    #文字列から日付型に変換(date)
    #post_date = datetime.strptime(post_date, "%Y-%m-%d")
    new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                    health=health,weight=weight,
                    detail=detail,post_date=dt_now,thred=id)
        
    db.session.add(new_post)
    db.session.commit()
    return redirect('/detail/'+str(id))
    


#
#編集完了ページ
#
@app.route('/arrangeFin/<int:id>',methods=['GET', 'POST'])
def arrangeFin(id):
    post = Post.query.get(id)
    """"
    passlength = request.form.get("passward")
    #パスワードの文字数が８文字以下、２１文字以上のときやり直しさせる
    if(len(passlength)<8):
        return render_template('arrange.html', post=post,passlength=1)
    elif(len(passlength)>20):
        return render_template('arrange.html', post=post,passlength=2)
    else:
    """
    #フォームからデータの入力、仮の初期値
    user = request.form.get('user',"nanasi")
    health=request.form.get('health',"good")
    weight=request.form.get('weight',"00")
    breakf = request.form.get('breakf',"今日の朝食")
    lunch=request.form.get('lunch',"今日の朝食")
    dinner=request.form.get('dinner',"今日の朝食")
    detail = request.form.get('detail',"ヤマザキパン")
    post_date = request.form.get("post_date","2021-12-31")
    dt_now = datetime.now()

    #文字列から日付型に変換(date)
    post_date = datetime.strptime(post_date, "%Y-%m-%d")
    #元のデータベースを上書き
    post.user=user 
    post.health=health
    post.weight=weight
    post.breakf=breakf
    post.lunch=lunch
    post.dinner=dinner
    post.detail=detail
    post.post_date=dt_now
    db.session.commit()
    return redirect('/calendar')
    
    

@app.route('/calendar')
def calender():
    return render_template('calendar.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)