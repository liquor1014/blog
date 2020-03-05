import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

#初始化程序和数据库

app = Flask(__name__)   #创建应用程序对象；
basedir = os.path.abspath(os.path.dirname(__file__))  #获取当前目录的绝对路径；
# print(__file__)
# print(basedir)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'myblog.db')  #sqlite数据库的文件存放路径
db = SQLAlchemy(app)

#定义博客文章数据Model类
class Blog(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String(50))
    text = db.Column(db.Text)

    def __init__(self,title,text):  #初始化方法
        self.title = title
        self.text = text

# db.create_all()  #创建数据库文件和数据库表，但只需操作一次


@app.route('/')
def home():
    '''
    渲染首页HTML模板文件
    '''
    return render_template('home.html')

app.run()