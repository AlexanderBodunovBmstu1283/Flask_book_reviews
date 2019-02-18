from header_footer import header_footer_
from app import app
import view

def permissions(func_):
    def wrapper(user,*args):
        if user.permissions=="admin":
            return func_(*args)
        else:
            return "Для выполнения данного действия нужны права администратора"
    return wrapper

def header_footer(func_):
    def wrapper(*args):
        pass
    return wrapper


if __name__=="__main__":
    app.run(debug=True)


