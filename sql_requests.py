from pymysql.err import MySQLError
from time import sleep

def try_to_exicute(number_of_times):
    def inner_(func_):
        def wrapper(*args, **kwargs):
            wrapper.__name__ = func_.__name__
            for i in range(number_of_times):
                try:
                    return func_(*args, **kwargs)
                except MySQLError as e:
                    sleep(0.01)
                    with open ("sql_error_log.txt","a+") as file:
                        file.write('Got error {!r}, errno is {}'.format(e, e.args[0])+"\n")
            return ["Запрос выполнился с ошибкой"]
        return wrapper
    return inner_

def execute_sql(querry,cursor):
    result=cursor.execute(querry)
    if result>0:
        return cursor.fetchall()
    else:
        return []

def execute_insert(querry,conn):
    pass

@try_to_exicute(3)
def ten_resent_reviews(cursor):
    return execute_sql("SELECT reviewer_name,review_title , text,book_title,type from rewiews_all ORDER BY id DESC LIMIT 10",cursor)

@try_to_exicute(3)
def select_books_faces(book_title,cursor):
    return execute_sql("SELECT image_face,id from books WHERE title = '{}' LIMIT 1".format(book_title),cursor)

@try_to_exicute(3)
def select_one_book(book_id,cursor):
    return execute_sql("SELECT * FROM books where id=" + str(book_id) + " LIMIT 1",cursor)

@try_to_exicute(3)
def select_reviews_to_book(title,cursor):
    return execute_sql("SELECT * FROM rewiews_all WHERE book_title = '{}'".format(title),cursor)

@try_to_exicute(3)
def select_comments_to_book(title,cursor):
    return execute_sql("SELECT * FROM comments WHERE book_title = '{}'".format(title),cursor)

@try_to_exicute(3)
def select_revews_by_book(title,cursor):
    return execute_sql("SELECT * FROM rewiews_all WHERE book_title = '{}' AND type!='отзыв'".format(title),cursor)

@try_to_exicute(3)
def select_comments_by_book(title,cursor):
    return execute_sql("SELECT * FROM comments WHERE book_title = '{}'".format(title),cursor)

@try_to_exicute(3)
def select_ten_reviews_of_category(category,cursor):
    return execute_sql("SELECT * FROM rewiews_all WHERE type = '{}' LIMIT 10".format(category),cursor)

@try_to_exicute(3)
def select_list_authors(cursor):
    return execute_sql("SELECT DISTINCT author FROM books",cursor)

@try_to_exicute(3)
def select_list_books(cursor):
    return execute_sql("SELECT title FROM books",cursor)

@try_to_exicute(3)
def select_books_by_author(author,cursor):
    return execute_sql("SELECT * FROM books WHERE author='{}'".format(author),cursor)

@try_to_exicute(5)
def try_to_exicute_by_author(request,cursor):
    return execute_sql("SELECT * FROM books WHERE MATCH (`author`) AGAINST('{}')".format(request),cursor)

@try_to_exicute(5)
def try_to_exicute_by_book(request,cursor):
    return execute_sql("SELECT * FROM books WHERE MATCH (`title`) AGAINST('{}')".format(request),cursor)

@try_to_exicute(3)
def select_random_capture(cursor):
    return execute_sql("SELECT photo,value FROM captures ORDER BY RAND() LIMIT 1",cursor)

@try_to_exicute(5)
def insert_user_review(user,text,conn):
    return execute_insert("INSERT INTO ",conn)
