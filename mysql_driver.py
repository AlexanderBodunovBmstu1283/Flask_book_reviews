# _*_ coding: utf-8 _*_
import pymysql

conn=pymysql.connect("localhost", "root", "", "poems_blog")

with conn:
    cur=conn.cursor()
    cur.execute("SELECT VERSION()")

    version=cur.fetchone()
    print("Database version {}".format(version[0]))