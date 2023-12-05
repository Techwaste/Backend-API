from fastapi import FastAPI, Body, Depends, File, UploadFile, Request
from fastapi.responses import FileResponse
from app.auth.jwt_bearer import jwtBearer
from app.auth.jwt_handler import *
from google.cloud import storage
from dotenv import load_dotenv
from connection import *
from app.model import *
from io import BytesIO
import mysql.connector
from app.function import *
from PIL import Image
import requests
import uvicorn
import random
import json
import jwt
import os
import io
import numpy as np


def decode_user(token2):
    decoded_data = jwt.decode(token2, JWT_SECRET, JWT_ALGORITHM)
    return decoded_data

# function.py


def searchUserById(id):
    mydb = defineDB()
    mycursor = mydb.cursor()
    values = (id,)
    mycursor.execute("SELECT * FROM users2 WHERE id= %s", values)
    # mycursor.execute("SELECT * FROM componenttable WHERE email='dgerbi11@answers.com'")

    myresult = mycursor.fetchall()
    name = myresult[0][1]
    mycursor.close()
    close_db_connection(mydb)
    return name


def getAllForum():
    mydb = defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM forum ORDER BY id DESC;")

    myresult = mycursor.fetchall()
    forumList = []
    for x in myresult:
        artic = {
            "id": x[0],
            "title": x[1],
            "category": x[2],
            "location": x[3],
            "content": x[4],
            "imageURL": x[5],
            "likes": x[6]
        }
        forumList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return forumList


def getForumName(forumName):
    mydb = defineDB()
    values = (forumName,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM forum WHERE title LIKE %s;", values)

    myresult = mycursor.fetchall()
    forumList = []
    for x in myresult:
        artic = {
            "id": x[0],
            "title": x[1],
            "category": x[2],
            "location": x[3],
            "content": x[4],
            "imageURL": x[5],
            "likes": x[6],
            "Postedby": searchUserById(x[7])
        }

        forumList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return forumList


def getArticleName(articleName):
    mydb = defineDB()
    values = (articleName,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM articles WHERE name LIKE %s;", values)

    myresult = mycursor.fetchall()
    forumList = []
    for x in myresult:
        artic = {
            "id": x[0],
            "name": x[1],
            "description": x[2],
            "articleImageURL": x[3],
            "componentID": x[4],
        }

        forumList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return forumList


def getForumByCategory(cate):
    mydb = defineDB()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT * FROM forum WHERE category = %s ORDER BY id DESC", (cate,))

    myresult = mycursor.fetchall()
    forumList = []
    for x in myresult:
        artic = {
            "id": x[0],
            "title": x[1],
            "category": x[2],
            "location": x[3],
            "content": x[4],
            "imageURL": x[5],
            "likes": x[6],
            "Postedby": searchUserById(x[7])
        }

        forumList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return forumList


def getForumById(desuwa):
    mydb = defineDB()
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT * FROM forum WHERE id =%s ORDER BY id DESC", (desuwa,))

    myresult = mycursor.fetchall()
    forumList = []

    artic = {
        "id": myresult[0][0],
        "title": myresult[0][1],
        "category": myresult[0][2],
        "location": myresult[0][3],
        "content": myresult[0][4],
        "imageURL": myresult[0][5],
        "likes": myresult[0][6],
        "Postedby": searchUserById(myresult[0][7])
    }

    forumList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return forumList


def postForumtest(forum: ForumSchema, token: str = Depends(jwtBearer())):
    print(token)
    mydb = defineDB()
    anu = decode_user(token)
    email = anu["userID"]
    mycursor = mydb.cursor()
    values = (email,)
    mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
    myresult = mycursor.fetchall()
    userId = myresult
    mycursor.close()
    close_db_connection(mydb)
    return userId


def check_user(data: UserLoginSchema):
    mydb = defineDB()
    mycursor = mydb.cursor()

    email = data.email
    password = data.password
    res = (email,)

    mycursor.execute("SELECT * FROM users2 WHERE email= %s", res)
    myresult = mycursor.fetchall()
    mycursor.close()
    close_db_connection(mydb)
    if (len(myresult) == 1):
        res_pass = myresult[0][3]
        if (password == res_pass):
            return True
    return False


def getCreden(data: UserLoginSchema):
    mydb = defineDB()
    if check_user(data):
        mycursor = mydb.cursor()
        email = data.email
        res = (email,)
        mycursor.execute("SELECT * FROM users2 WHERE email= %s", res)
        myresult = mycursor.fetchall()
        resId = myresult[0][0]
        resName = myresult[0][1]
        mycursor.close()
        close_db_connection(mydb)
        return {
            "id": resId,
            "Username": resName
        }
    else:
        return {"error": "what the hell are you trying to do 🗿"}


def pushUser(data: UserSchema):
    mydb = defineDB()
    mycursor = mydb.cursor()

    name = data.fullname
    email = data.email
    password = data.password
    resq = (email,)

    mycursor.execute("SELECT * FROM users2 WHERE email= %s", resq)

    myresult = mycursor.fetchall()

    isTaken = "undefined"

    if (len(myresult) == 1):
        isTaken = True
    else:
        isTaken = False

    if (isTaken):
        mycursor.close()
        close_db_connection(mydb)

        return False
    else:
        query = "insert into users2 (name, email, password) values (%s, %s, %s);"
        res = (name, email, password)
        mycursor.execute(query, res)
        mydb.commit()
        mycursor.close()
        close_db_connection(mydb)

        return True


def getbyId(id):
    mydb = defineDB()
    mycursor = mydb.cursor()

    # mycursor.execute("SELECT * FROM3 comps")
    res = (id,)
    mycursor.execute("SELECT * FROM comps WHERE id= %s", res)

    myresult = mycursor.fetchall()
    id = myresult[0][0]
    name = myresult[0][1]
    desc = myresult[0][2]
    example = myresult[0][3]

    myresult = {
        "id": id,
        "name": name,
        "desc": desc,
        "example": example
    }
    mycursor.close()
    close_db_connection(mydb)
    return myresult


def getArticlebyId(compid):
    mydb = defineDB()
    mycursor = mydb.cursor()
    res = (compid,)
    mycursor.execute("SELECT * FROM articles WHERE componentId= %s", res)
    myresult = mycursor.fetchall()
    articleList = []
    for t in myresult:
        artic = {
            "id": t[0],
            "name": t[1],
            "desc": t[2],
            "articleImageURL": t[3],
            "componentId": t[4]
        }
        articleList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return articleList


def getAllArticleby():
    mydb = defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM articles ORDER BY id DESC;")
    myresult = mycursor.fetchall()
    articleList = []
    for t in myresult:
        artic = {
            "id": t[0],
            "name": t[1],
            "desc": t[2],
            "articleImageURL": t[3],
            "componentId": t[4]
        }
        articleList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return articleList


def getAllComponents():
    mydb = defineDB()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM comps ORDER BY id DESC;")
    myresult = mycursor.fetchall()
    articleList = []
    for t in myresult:
        artic = {
            "id": t[0],
            "name": t[1],
            "desc": t[2],
            "imageExample": t[3],
        }
        articleList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return articleList


def getArticleID2(articleName):
    mydb = defineDB()
    values = (articleName,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM articles WHERE id=%s;", values)

    myresult = mycursor.fetchall()
    forumList = []
    for x in myresult:
        compID = (x[4],)
        mycursor2 = mydb.cursor()
        mycursor2.execute("SELECT * FROM comps WHERE id=%s;", compID)
        myresult2 = mycursor2.fetchall()
        artic = {
            "id": x[0],
            "name": x[1],
            "description": x[2],
            "articleImageURL": x[3],
            "componentID": x[4],
            "componentName": myresult2[0][1]
        }

        forumList.append(artic)
    mycursor.close()
    mycursor2.close()
    close_db_connection(mydb)
    return forumList


def postForum(forum: ForumSchema, email):
    mydb = defineDB()
    mycursor = mydb.cursor()
    values = (email,)
    mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
    myresult = mycursor.fetchall()
    userId = myresult[0][0]
    lilcursorhehe = mydb.cursor()
    query = "insert into forum (title, category, location, content, imageUrl, userId) values (%s, %s, %s, %s, %s, %s);"
    res = (forum.title, forum.category, forum.location,
           forum.content, forum.imageUrl, userId)
    lilcursorhehe.execute(query, res)
    mydb.commit()
    mycursor.close()
    lilcursorhehe.close()
    close_db_connection(mydb)
    return {
        "error": "false",
        "message": "your post has been posted 😱🥶🥶🥶🥶🥶🥶🥶"
    }


def getCommentForum(forumid):
    mydb = defineDB()
    values = (forumid,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM comment WHERE forumID LIKE %s;", values)

    myresult = mycursor.fetchall()
    commentList = []
    for x in myresult:
        artic = {
            "id": x[0],
            "comment": x[1],
            "userID": x[2],
            "username": x[3],
            "replyFrom": x[4],
            "forumID": x[5]
        }

        commentList.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return commentList


def postComment(input: CommentSchema, email):
    mydb = defineDB()
    mycursor = mydb.cursor()
    values = (email,)
    mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
    myresult = mycursor.fetchall()
    userId = myresult[0][0]
    username = myresult[0][1]
    lilcursorhehe = mydb.cursor()
    query = "insert into comment (comment, userID, username, replyFrom, forumID) values (%s, %s, %s, %s, %s);"
    res = (input.comment, userId, username, 0, input.forumID)
    lilcursorhehe.execute(query, res)
    mydb.commit()
    mycursor.close()
    lilcursorhehe.close()
    close_db_connection(mydb)
    return {
        "error": "false",
        "message": "your comment has been posted 😱🥶🥶🥶🥶🥶🥶🥶",
        "commentInfo": {
            "Poster": username,
            "PosterID": userId,
            "forumID": input.forumID,
            "comment": input.comment
        }
    }


def replybyCommentID(input: ReplySchema, email):
    mydb = defineDB()
    mycursor = mydb.cursor()
    values = (email,)
    mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
    myresult = mycursor.fetchall()
    userId = myresult[0][0]
    username = myresult[0][1]
    lilcursorhehe = mydb.cursor()
    query = "insert into comment (comment, userID, username, replyFrom, forumID) values (%s, %s, %s, %s, %s);"
    res = (input.comment, userId, username, input.replyFrom, input.forumID)
    lilcursorhehe.execute(query, res)
    mydb.commit()
    mycursor.close()
    lilcursorhehe.close()
    close_db_connection(mydb)
    return {
        "error": "false",
        "message": "your comment has been posted 😱🥶🥶🥶🥶🥶🥶🥶",
        "commentInfo": {
            "Poster": username,
            "PosterID": userId,
            "forumID": input.forumID,
            "comment": input.comment
        }
    }


def getSmallPartsComp(compid):
    mydb = defineDB()
    values = (compid,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM smallParts WHERE compID = %s;", values)

    myresult = mycursor.fetchall()
    smallParts = []
    for x in myresult:
        artic = {
            "id": x[0],
            "name": x[1],
            "description": x[2],
            "imageURL": x[3],
            "compID": x[4],
        }

        smallParts.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return smallParts


def getSmallPartsComp(id):
    mydb = defineDB()
    values = (id,)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM smallParts WHERE id = %s;", values)

    myresult = mycursor.fetchall()
    smallParts = []
    for x in myresult:
        artic = {
            "id": x[0],
            "name": x[1],
            "description": x[2],
            "imageURL": x[3],
            "compID": x[4],
        }
        smallParts.append(artic)
    mycursor.close()
    close_db_connection(mydb)
    return smallParts


def postForum(forum: ForumSchema, email):
    mydb = defineDB()
    mycursor = mydb.cursor()
    values = (email,)
    mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
    myresult = mycursor.fetchall()
    userId = myresult[0][0]
    lilcursorhehe = mydb.cursor()
    query = "insert into forum (title, category, location, content, imageUrl, userId) values (%s, %s, %s, %s, %s, %s);"
    res = (forum.title, forum.category, forum.location,
           forum.content, forum.imageUrl, userId)
    lilcursorhehe.execute(query, res)
    mydb.commit()
    mycursor.close()
    lilcursorhehe.close()
    close_db_connection(mydb)
    return {
        "error": "false",
        "message": "your post has been posted 😱🥶🥶🥶🥶🥶🥶🥶"
    }


# LIKE SYSTEM

def convert_string_to_array(input_string):
    # Check if input_string is None
    if input_string is None:
        return np.array([])  # Return an empty array if input_string is None

    # Remove the brackets from the string
    input_string = input_string.strip('[]')
    # Split the string into individual numbers
    numbers = input_string.split()
    # Convert the numbers from strings to integers using NumPy
    array = np.array(numbers, dtype=int)
    return array


def convert_array_to_string(array):
    # Check if array is None
    if array is None:
        return ""  # Return an empty string if array is None

    # Convert the array elements to strings
    string_elements = [str(element) for element in array]
    # Join the elements with spaces
    string_representation = " ".join(string_elements)
    # Add brackets around the string
    string_representation = "[" + string_representation + "]"
    return string_representation


def is_value_present(array, value):
    # Check if value is already in the array
    return np.isin(value, array)


def check_value_status(input_string, value_to_check):
    array = convert_string_to_array(input_string)

    if is_value_present(array, value_to_check):
        return True
    else:
        return False


def add_value_to_array(input_string, value_to_push):
    array = convert_string_to_array(input_string)

    if is_value_present(array, value_to_push):
        return "already liked"
    else:
        if array.size == 0:
            result_array_pushed = np.array([value_to_push])
        else:
            # Push the value into the array
            result_array_pushed = np.append(array, value_to_push)

        result_string_pushed = convert_array_to_string(result_array_pushed)
        return result_string_pushed
