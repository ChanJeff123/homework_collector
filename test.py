#-*- coding: UTF-8 -*-
import re
import sys
import os
import Tkinter
import csv
import sqlite3
import random
import time



'''
1.读入班级学号和名字
2.选择名字，录入卡号
3.统计作业。打卡录入数据库
4.数据库查询

表1,stdnt_id
学号，姓名
表2,stdnt_rfid
学号，rfid卡号
表3,stdnt_homework
日期，rfid卡号




'''


mylist = None
stdnt_list = []
index_stdnt = -1

def readRfid():
    import RPi.GPIO as GPIO
    import SimpleMFRC522
    reader = SimpleMFRC522.SimpleMFRC522()
    id = ''
    try:
        id, text = reader.read()
        print(id)
        print(text)
    finally:
        GPIO.cleanup()
    return id

def addStdnt():
    # 读取csv至字典
    csvFile = open("name.csv", "r")
    reader = csv.reader(csvFile)
    # 建立空字典
    result = {}
    for item in reader:
        # 忽略第一行
        # if reader.line_num == 1:
        #     continue
        result[item[0]] = item[1]
        
    csvFile.close()
    # print(result)

    # 添加学生
    conn = sqlite3.connect('homework.db')
    c = conn.cursor()
    try:
        for i in result:
            print i, result[i]
            c.execute("INSERT INTO stdnt_id (stdnt_id,name) \
                VALUES ('%s', '%s')" % (i, result[i]));
        conn.commit()
    finally:
        conn.close()


def showStdnt():
    global mylist
    global stdnt_list
    global index_stdnt
    index_stdnt = -1
    stdnt_list = []
    conn = sqlite3.connect('homework.db')
    print "Opened database successfully"
    c = conn.cursor()

    # SELECT 操作
    cursor = c.execute("SELECT stdnt_id, name from stdnt_id ORDER BY stdnt_id")
    result2 = []
    for row in cursor:
        print "stdnt_id = ", row[0]
        print "name = ", row[1],"\n"
        result2.append('%s_%s' % (row[0], row[1]))
        stdnt_list.append([row[0], row[1]])
    print cursor
    a = cursor.fetchall()
    print a

    conn.commit()
    conn.close()

    win = Tkinter.Tk()
    win.title("名单")
    Tkinter.Label(win, text='名单', fg='red').pack()
    mylist=Tkinter.Listbox(win, width=20) #列表框
    mylist.pack()
    for item in result2: #插入内容
        mylist.insert(Tkinter.END, item) #从尾部插入

    #设置表格的项目颜色等
    for i in range(len(result2)):
        mylist.itemconfig(i,fg="blue")
        if not i%2:
            mylist.itemconfig(i,bg="#f0f0ff")

    # 设置绑定事件
    mylist.bind("<<ListboxSelect>>", addHomework)
    Tkinter.Button(win, text="添加rfid卡", width=20, command=addRfid, bg="blue").pack()
    win.mainloop()

def collectHomework():
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 到数据库中查找，如果有这个卡，则记录一条作业
    conn = sqlite3.connect('homework.db')
    c = conn.cursor()
    # 添加一个作业
    try:
        c.execute("INSERT INTO homework_date (date) VALUES ('%s')" % date);
    finally:
        # SELECT 操作
        rfid = readRfid()
        cursor = c.execute("SELECT stdnt_id FROM stdnt_rfid WHERE stdnt_rfid = '%s'" % rfid)
        a = cursor.fetchall()
        if len(a) > 0:
            print a[0][0]
            try:
                tmp1 = c.execute("SELECT * FROM stdnt_homework")
                tmp2 = tmp1.fetchall()
                tmp3 = len(tmp2)
                c.execute("INSERT INTO stdnt_homework (id,date,stdnt_rfid) VALUES (%d,'%s','%s')" % (int(tmp3+1), date, rfid) );
                conn.commit()
            finally:
                pass
        else:
            print "未录入的rfid"
        conn.close()

def addHomework(*args):
    global mylist
    global stdnt_list
    global index_stdnt
    indexs = mylist.curselection()
    index = int(indexs[0])
    print stdnt_list[index][0], stdnt_list[index][1]
    index_stdnt = index


def addRfid():
    global mylist
    global stdnt_list
    global index_stdnt
    print index_stdnt
    conn = sqlite3.connect('homework.db')
    c = conn.cursor()
    try:
        rfid = readRfid()
        c.execute("INSERT INTO stdnt_rfid (stdnt_rfid,stdnt_id) \
            VALUES ('%s', '%s')" % (rfid, stdnt_list[index_stdnt][0]));
        conn.commit()
    finally:
        conn.close()

# 创建表
def createTable():
    conn = sqlite3.connect('homework.db')
    print "Opened database successfully"
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE stdnt_id
            (stdnt_id     text     PRIMARY KEY     NOT NULL,
            name    text    NOT NULL);''')
        c.execute('''CREATE TABLE stdnt_rfid
            (stdnt_rfid     text     PRIMARY KEY     NOT NULL,
            stdnt_id    text    NOT NULL);''')
        c.execute('''CREATE TABLE stdnt_homework
            (id     int     PRIMARY KEY     NOT NULL,
            date    text    NOT NULL,
            stdnt_rfid    text    NOT NULL);''')
        c.execute('''CREATE TABLE homework_date
            (date     text     PRIMARY KEY     NOT NULL);''')
        conn.commit()
        print "Table created successfully"
    finally:
        conn.close()

# 删除所有表
def deleteTable():
    conn = sqlite3.connect('homework.db')
    print "Opened database successfully"
    c = conn.cursor()
    try:
        c.execute('drop table stdnt_id;')
        c.execute('drop table stdnt_rfid;')
        c.execute('drop table stdnt_homework;')
        c.execute('drop table homework_date;')
        conn.commit()
    finally:
        conn.close()

# 清空表
def deleteData():
    conn = sqlite3.connect('homework.db')
    print "Opened database successfully"
    c = conn.cursor()
    try:
        c.execute('delete from stdnt_id;')
        c.execute('delete from stdnt_rfid;')
        c.execute('delete from stdnt_homework;')
        c.execute('delete from homework_date;')
        conn.commit()
    finally:
        conn.close()


# 检查stdnt_homework中，是否有交作业记录。有返回true，否则返回false
def checkHomework(date, rfid):
    conn = sqlite3.connect('homework.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM stdnt_homework WHERE date = '%s' AND stdnt_rfid = '%s'" % (date, rfid))
    a = cursor.fetchall()
    conn.commit()
    conn.close()
    return len(a) > 0

# 返回一个学生的所有rfid卡
def getStudentRfid(stdnt_id):
    result = []
    conn = sqlite3.connect('homework.db')
    c = conn.cursor()
    cursor = c.execute("SELECT stdnt_rfid FROM stdnt_rfid WHERE stdnt_id = '%s'" % stdnt_id)
    for row in cursor:
        print "stdnt_rfid = ", row[0]
        result.append('%s' % row[0])
    conn.commit()
    conn.close()
    return result

def showHomework():
    # print getStudentRfid('010')
    # print checkHomework('2019-04-14', '749197')
    date = time.strftime("%Y-%m-%d", time.localtime())
    conn = sqlite3.connect('homework.db')
    print "Opened database successfully"
    c = conn.cursor()

    # SELECT 操作
    cursor = c.execute("SELECT stdnt_id, name from stdnt_id ORDER BY stdnt_id")
    # print cursor
    # a = cursor.fetchall()
    # print a
    result2 = []
    result3 = []
    result4 = []
    for row in cursor:
        print "stdnt_id = ", row[0]
        print "name = ", row[1],"\n"
        result2.append('%s_%s' % (row[0], row[1]))
        result3.append(row[0])
    conn.commit()
    conn.close()

    for i in range(len(result3)):
        # 查找rfid
        stdnt_id = result3[i]
        tmp1 = getStudentRfid(stdnt_id)
        tmp2 = False
        for j in range(len(tmp1)):
            rfid = tmp1[j]
            if checkHomework(date, rfid):
                tmp2 = True
                break
        result4.append(tmp2)

    win = Tkinter.Tk()
    win.title("名单")
    Tkinter.Label(win, text='名单', fg='red').pack()
    mylist=Tkinter.Listbox(win, width=20) #列表框
    mylist.pack()
    for item in result2: #插入内容
        mylist.insert(Tkinter.END, item) #从尾部插入

    #设置表格的项目颜色等
    for i in range(len(result4)):
        if result4[i] == True:
            mylist.itemconfig(i,fg="green")
        else:
            mylist.itemconfig(i,fg="red")

    # 设置绑定事件
    win.mainloop()

if __name__ == '__main__':
    root = Tkinter.Tk()
    root.title("作业系统")
    Tkinter.Label(root, text='作业系统', fg='red').pack()
    # 添加学生，添加作业，开始收作业，
    Tkinter.Button(root, text="创建表", width=20, command=createTable, bg="blue").pack()
    Tkinter.Button(root, text="删除表", width=20, command=deleteTable, bg="blue").pack()
    Tkinter.Button(root, text="清空表", width=20, command=deleteData, bg="blue").pack()
    Tkinter.Button(root, text="添加学生", width=20, command=addStdnt, bg="blue").pack()
    Tkinter.Button(root, text="学生列表", width=20, command=showStdnt, bg="green").pack()
    Tkinter.Button(root, text="收作业", width=20, command=collectHomework, bg="red").pack()
    Tkinter.Button(root, text="作业统计", width=20, command=showHomework, bg="yellow").pack()
    root.mainloop()

