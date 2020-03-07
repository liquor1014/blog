import os
from flask import Flask, render_template, request, redirect
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

    def __repr__(self):
        return self.title + ":" + self.text


# db.create_all()  #创建数据库文件和数据库表，但只需操作一次


@app.route('/')
def home_blog():
    '''
    渲染首页HTML模板文件
    '''
    return render_template('home.html')

#查询博文全部列表
@app.route('/blogs',methods=['GET'])
def list_blog():
    blogs = Blog.query.all()
    return  render_template('list.html',blogs = blogs)

#创建blog文章
@app.route('/blogs/create',methods=['GET','POST'])
def write_blog():
    if request.method == 'GET':
        return render_template('write.html')
    else:
        title = request.form['title']   #request.from获取以post方式提交的数据
        text = request.form['text']

    #创建一个blog对象
        blog = Blog(title = title , text = text)
        db.session.add(blog)
        db.session.commit()     # 必须提交才能生效
        return redirect('/blogs')   # 创建完成之后重定向到博文列表页面

#blog详情和删除
@app.route('/blogs/<uid>', methods=['GET','DELETE'])
def del_inquire_blog(uid):
    if request.method == 'GET':
        blog = Blog.query.filter_by(id =uid).first_or_404()

        return render_template('query_blog.html', blog=blog)
    elif request.method == 'DELETE':
        blog = Blog.query.filter_by(id =uid).delete()
        db.session.commit()
        return 'ok'

@app.route('/blogs/update/<id>',methods = ['GET', 'POST'])
def update_note(id):
    '''
    更新博文
    '''
    if request.method == 'GET':
        # 根据ID查询博文详情
        blog = Blog.query.filter_by(id = id).first_or_404()
        # 渲染修改笔记页面HTML模板
        return render_template('update_blog.html',blog = blog)
    else:
        # 获取请求的博文标题和正文
        title = request.form['title']
        text = request.form['text']

        # 更新博文
        blog = Blog.query.filter_by(id = id).update({'title':title,'text':text})
        # 提交才能生效
        db.session.commit()
        # 修改完成之后重定向到博文详情页面
        return redirect('/blogs/{id}'.format(id = id))

app.run()