import sql_requests

def return_search(cursor,request):
    #key_words=["Книга","книга","Роман"]
    #request=request
    #authors=cursor.exicute(sql_requests.select_list_authors())
    #authors=authors.fethall() if authors>0 else []
    #books=cursor.exicute(sql_requests.select_list_books())
    #books=books.fethall() if books>0 else []

    title_try=sql_requests.try_to_exicute_by_book(request,cursor)
    #title_try=cursor.fetchall(title_try)
    if len(title_try)>0:
        return title_try,"book"
    else:
        author_try=sql_requests.try_to_exicute_by_author(request,cursor)
        #author_try = cursor.fetchall(author_try)
        if len(author_try)>0:
            return author_try,"author"
    return ["Ничего не нашлось"],"nothing"