from flask import render_template,request,redirect,url_for
from flask_mysqldb import MySQL
import pymysql.cursors
import os
import sql_requests
import search

from app import app
from header_footer import header_footer_
import os

APP_ROOT=os.path.dirname(os.path.abspath(__file__))

def tag_pack(tag,class_=None,id_=None):
    def inner_(func_):
        def wrapper(*args, **kwargs):
            return "<{0} {1} {2}> {3} </{0}>".format(tag, "class=" + class_ if class_ != None else "","id=" + id_ if id_ != None else "", func_(*args, **kwargs))
        wrapper.__name__=func_.__name__
        return wrapper
    return inner_

def add_ref(ref_,text_):
    return "<a href={0}><button>{1}</button></a>".format(ref_,text_)


@tag_pack("div","main_article")
def main_article():
    with open("static/main_article.txt") as file:
        content=file.read().split("\n")
    article_main={"title":content[0],"anotation":content[1],"text":" ".join(content[1:])}

    #main_image=os.path.join(app.config['UPLOAD_FOLDER'],'static_images/image1.jpg')
    #main_image=
    #return "Main_article</br><img src= '{{url_for('static',filename='image1.jpg')}}' />"
    return render_template('main.html',article_main=article_main)+add_ref("upload","обновить новость")


def display_posts(posts):
    result=""
    for i in posts:
        result+="<div class='post'>"
        for key in i:
            if key=='id':
                pass
            if key=='title':
                result+="<p style='font-size: 1.5em'><b>"+str(i[key])+"</b></p>"
            if key=='date':
                result+="<p style='color: blue'>"+str(i[key])+"</p>"
            if key=='text':
                result += "<p>" + str(i[key]) + "</p>"
        result += "</div>"
    return result


def connect():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='poems_blog',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@tag_pack("div","news")
def news():
    connection=connect()
    try:
        with connection.cursor() as cursor:
            result_value=cursor.execute("SELECT * FROM news")
            if result_value>0:
                data=cursor.fetchall()
            else:
                data=[]
            cursor.close()

    except:
        return "error"
    return "Новости: </br>" + display_posts(data)

@tag_pack("div","slider_photo")
def photo_slider():
    return render_template('slider.html')


@tag_pack("div","slider_photo")
def photo_slider_1():
    photos=os.listdir("static/slider_images")
    photos=[{"url":"slider_images/"+i,"name":"author/"+i.split(".")[0]} for i in photos]
    return render_template('slider_1.html',photos=photos)

@tag_pack("div","particle")
def particle():
    return ""


def show_books(book_id,capture):
    connection = connect()

    with connection.cursor() as cursor:
            data = sql_requests.select_one_book(book_id,cursor)
            if len(data) > 0:
                data=data[0]
                #data = cursor.fetchall()[0]
                title=data["title"]
                reviews=sql_requests.select_revews_by_book(title,cursor)
                data["reviews"] = reviews
                comments = sql_requests.select_comments_by_book(title,cursor)
                data["comments"] = comments
            else:
                data = []
            cursor.close()
    return "Книги: </br>" + render_template('books.html',book=data,capture=capture)

@app.route('/')
@header_footer_
@tag_pack("div","slidebar","main")
def index():
    connection=connect()
    with connection.cursor() as cursor:
            if 'type' in request.args:
                category_=request.args.get('type')
                reviews = sql_requests.select_ten_reviews_of_category(category_,cursor)
            else:
                reviews = sql_requests.ten_resent_reviews(cursor)

            for i in range(len(reviews)):
                with open ("try_log.txt","a+") as file:
                    file.write("{}\n".format(reviews[i]))
                image_face= sql_requests.select_books_faces(reviews[i]["book_title"],cursor)
                reviews[i]["image_face"]=image_face[0] if len(image_face)>0 else []


    return render_template('index.html',reviews=reviews)


@app.route('/author',methods=["GET","POST"])
@header_footer_
@tag_pack("div","slidebar","main")
def author():
    if 'books' in request.args:
        books=request.args.get('books')
        with open ("books.txt","w")as file:
            file.write("{}".format(books))
        books=[eval(books)]
        #return"{}".format(books)
        return render_template('author.html',books=books)


@app.route('/search_querry',methods=["GET","POST"])
def search_querry():
    connection = connect()
    with connection.cursor() as cursor:
        if request.method == "POST":
            search_ = request.form['input']
            materials, type = search.return_search(cursor, search_)
            if len(materials) > 0:
                if type == "book":
                    return redirect(url_for('book',id=materials[0]["id"]))
                else:
                    if type == "author":
                        return redirect(url_for('author',books=[materials]))
            return "Ничегошеньки"


@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method=="POST":
        target=os.path.join(APP_ROOT,"static/")
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        file=request.files['file']
        filename="main_image.jpg"
        destination="/".join([target,filename])
        print(destination)
        file.save(destination)
        return "Запись обновлена <br>"+add_ref("../","Вернуться на главную")
    else:
        return render_template('upload.html')

@app.route("/book",methods=["GET","POST"])
@header_footer_
@tag_pack("div","slidebar")
def book():
    connection = connect()
    with connection.cursor() as cursor:
        book_id=request.args.get('id')
        capture=sql_requests.select_random_capture(cursor)[0]
        return show_books(book_id,capture)