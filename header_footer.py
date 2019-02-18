from flask import render_template

def tag_pack(tag,class_=None,id_=None):
    def inner_(func_):
        def wrapper(*args, **kwargs):
            return "<{0} {1} {2}> {3} </{0}>".format(tag,"class="+class_ if class_!=None else "","id="+class_ if id_!=None else "",func_(*args, **kwargs))
        return wrapper
    return inner_

def pack_v(var_,tag_):
    return "<{0}> {1} </{0}>".format(tag_, var_)

def pack_ref(var_,ref_):
    return "<a href={0}><button>{1}</button></a>".format(ref_, var_)


@tag_pack("div","header")
def pack_in_ul(feed_dict,class_=None,id_=None):
    proportion=int(1/len(feed_dict)*100)
    li_str="".join(["<li width='{}%'>".format(proportion)+pack_ref(key,feed_dict[key])+"</li>" for key in feed_dict])
    return "<ul {0} {1} > {2} </ul>".format("class="+class_ if class_!=None else "","id="+id_ if id_!=None else "",li_str)

def header_footer_(func_):
    def wrapper(*args,**kwargs):
        refs={"slidebar_1":{"На главную":"/","Рецензии":"/?type=рецензия","Отзывы":"/?type=отзыв","Критические обзоры":"/?type=критический_обзор"},
              "slidebar_2": {"Регистрация": "/registration", "Авторизация": "/autorization", "О нас": "/about"}}

        @tag_pack("head")
        def head_tag():
            return render_template("head.html")#"<link href='styles.css' type='text/css' rel='stylesheet' >"

        @tag_pack("header")
        def header():
            search=render_template("search.html")
            result=search+pack_in_ul(refs["slidebar_1"],"main top",id_="2")
            return result

        @tag_pack("footer")
        def footer():
            result = pack_in_ul(refs["slidebar_1"], "main top", id_="3")
            return result
        return head_tag()+header()+func_(*args,**kwargs)+footer()

    wrapper.__name__ = func_.__name__
    return wrapper





'''
result=pack_v(pack_ref("Авторы","/authors")+
pack_ref("Блоги","/blogs")+
pack_ref("События", "/events"),"div")
'''