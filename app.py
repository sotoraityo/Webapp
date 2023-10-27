from flask import Flask, render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,date
import time
import pandas as pd
from sqlalchemy.dialects import postgresql as pg
import os
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required
from werkzeug.security import generate_password_hash, check_password_hash
import graph

import os
import csv
import urllib.request
from bs4 import BeautifulSoup

from scraping import str2float,scraping,create_csv

"""
from main import app, db
with app.app_context():
  db.create_all()
"""
#%%
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

    wake_temp=db.Column(db.REAL,nullable=True)
    before_temp=db.Column(db.REAL,nullable=True)
    warm_temp=db.Column(db.REAL,nullable=True)
    after_temp=db.Column(db.REAL,nullable=True)
    bed_temp=db.Column(db.REAL,nullable=True)
    sihyovalue1=db.Column(db.Integer,nullable=True)
    sihyovalue2=db.Column(db.Integer,nullable=True)
    sihyovalue3=db.Column(db.Integer,nullable=True)
    sihyovalue4=db.Column(db.Integer,nullable=True)
    sihyovalue5=db.Column(db.Integer,nullable=True)

    thred = db.Column(db.Integer, nullable=False)

#%%
#メインページ
#
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


#%%
#目次ページ
#
@app.route('/index')
def index():
    #Postデータベースからすべての投稿を取り出す
    db.session.commit()
    posts=Post.query.filter(Post.thred==0)
    return render_template('index.html', posts=posts)



#%%
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

#%%
#ログインページ
#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/calendar')
    else:
        return render_template('login.html')

#%%
#ログアウトページ
#
@app.route('/logout')
#@login_required
def logout():
    #ユーザーをログアウトさせる
    logout_user()
    return redirect('/login')

#%%
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

        #日付が既にあるか確認
        posts=Post.query.filter(Post.post_date==select_date,Post.thred==0)
        check=posts.count()
        if check!=0:
            #既にあるなら詳細ページに移行
            id=posts[0].id
            return redirect('/detail/'+str(id))
        
        #無いなら投稿作成に移行
        return render_template('create.html',datenow=select_date)
    else:
        dt_now =datetime.now()
        return render_template('create.html',datenow=dt_now)


#%%
#投稿作成完了url
#
@app.route('/createupload', methods=['GET', 'POST'])
#@login_required
def main():
    if request.method=='GET':
        return redirect('/calendar')

    #Postのデータを読み取り、postdataにデータを保存し、newpostを作る
    else:
        #日付が既にあるか確認
        get_date = request.form.get("post_date","2023-10-10")# formから取得
        post_date = datetime.strptime(get_date, "%Y-%m-%d")
        posts=Post.query.filter(Post.post_date==post_date)# DBを確認
        
        #既にあるなら本当にするか確認
        if  posts.count():
            flash("既にありました＼(^o^)／", "failed")        
            return render_template('create.html',datenow=post_date)
            
        
        #フォームからデータの入力、仮の初期値
        user = request.form.get('user',"nanasi")
        health=request.form.get('health',"good")
        weight=request.form.get('weight',"00")
        breakf = request.form.get('breakf',"なし")
        lunch=request.form.get('lunch',"なし")
        dinner=request.form.get('dinner',"なし")
        detail = request.form.get('detail',"なし")
        post_date = request.form.get("post_date","2021-12-31")

        wake_temp= request.form.get('wake_temp',"35.0")
        before_temp= request.form.get('before_temp',"35.1")
        warm_temp= request.form.get('warm_temp',"35.2")
        after_temp= request.form.get('after_temp',"35.3")
        bed_temp= request.form.get('bed_temp',"35.4")
        sihyovalue1= request.form.get('sihyo1',"0")
        sihyovalue2= request.form.get('sihyo2',"0")
        sihyovalue3= request.form.get('sihyo3',"0")
        sihyovalue4= request.form.get('sihyo4',"0")
        sihyovalue5= request.form.get('sihyo5',"0")
        thred=0

        #文字列から日付型に変換(date)
        post_date = datetime.strptime(post_date, "%Y-%m-%d")

        new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                        health=health,weight=weight,
                        detail=detail,post_date=post_date,
                        wake_temp=wake_temp,before_temp=before_temp,
                        warm_temp=warm_temp,after_temp=after_temp,
                        bed_temp=bed_temp,
                        sihyovalue1=sihyovalue1,sihyovalue2=sihyovalue2,
                        sihyovalue3=sihyovalue3,sihyovalue4=sihyovalue4,
                        sihyovalue5=sihyovalue5,
                        thred=thred)
        
        db.session.add(new_post)
        db.session.commit()
        
        if post_date.strftime("%Y-%m-%d")!=date.today().strftime("%Y-%m-%d"):
            create_csv(post_date)
        return redirect('/calendar')


#%%
#詳細ページ　データベースのIDからデータを指定
#
@app.route('/detail/<int:id>')
def detail(id):
    #idの指定
    post = Post.query.get(id)
    comments=Post.query.filter(Post.thred==id)
    dt_now =datetime.now()
    return render_template('detail.html', post=post,comments=comments,datenow=dt_now)

#%%
#編集ページ
#
@app.route('/arrange/<int:id>',methods=['GET', 'POST'])
#@login_required
def arrange(id):
    #idのポストを取得
    post = Post.query.get(id)
    return render_template('arrange.html', post=post)
    
#%%
#削除ページ
#
@app.route('/delete/<int:id>',methods=['GET', 'POST'])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/calendar')
        
#%%
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
    #dt_now = datetime.now()

    #文字列から日付型に変換(date)
    post_date = datetime.strptime(post_date, "%Y-%m-%d")
    new_post = Post(user=user, breakf=breakf,lunch=lunch,dinner=dinner,
                    health=health,weight=weight,
                    detail=detail,post_date=post_date,thred=id)
        
    db.session.add(new_post)
    db.session.commit()
    return redirect('/detail/'+str(id))
    

#%%
#編集完了ページ
#
@app.route('/arrangeFin/<int:id>',methods=['GET', 'POST'])
def arrangeFin(id):
    post = Post.query.get(id)
 
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
    return redirect('/index')
    
#%% 
#カレンダーのページ
#
@app.route('/calendar',methods=['GET','POST'])
def calender():
    #投稿してある日付を取得、htmlにわたす
    #post_dates=Post.query(Post.post_date).all
    db.session.commit()
    post_dates=Post.query.filter(Post.thred==0)
    return render_template('calendar.html', post_dates=post_dates)
    
#%%
#画像アップロードのページ
#
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # GETではアップロードするページを
    if request.method == 'GET':
        return render_template('upload.html')
    
    # formでsubmitボタンが押されるとPOSTリクエストとなるのでこっち
    elif request.method == 'POST':
        #ファイルをrequestで受け取り、/uploadfileに受け渡す
        file = request.files['file_upload']
        file.save(os.path.join('./static/image', file.filename))
        #csvファイルの選択とファイル名の取得
        filecsv=request.files['csv_upload']
        csvname=filecsv.filename
        

        return redirect(url_for('uploadcheck', filename=file.filename,csvname=csvname))

#%%
@app.route('/uploadedcheck/<string:filename>/<string:csvname>')
def uploadcheck(filename,csvname):
    #usefile=url_for('./static', filename='csv/'+csvname)
    #usefile='./static/csv/Pulse_20230803-155420.csv'
    usefile='./static/csv/'+csvname
    graphfile=graph.csvplot(usefile)
    return render_template('uploadcheck.html', filename=filename,graphfile=graphfile)


#%%
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)