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

def decode_user(token2):
    decoded_data = jwt.decode(token2,JWT_SECRET,JWT_ALGORITHM)
    return decoded_data

#function.py
def searchUserById(id):
  mydb=defineDB()
  mycursor = mydb.cursor()
  values = (id,)
  mycursor.execute("SELECT * FROM users2 WHERE id= %s", values)
  # mycursor.execute("SELECT * FROM componenttable WHERE email='dgerbi11@answers.com'")

  myresult = mycursor.fetchall()
  name = myresult[0][1]
  mycursor.close()
  close_db_connection(mydb, "components")
  return name

def getAllForum():
  mydb=defineDB()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM forum ORDER BY id DESC;")

  myresult = mycursor.fetchall()
  forumList = []
  for x in myresult:
    artic = {
    "id":x[0],
    "title":x[1],
    "category":x[2],
    "location":x[3],
    "content":x[4],
    "imageURL":x[5],
    "likes":x[6]
    }
    forumList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return forumList

def getForumName(forumName):
  mydb=defineDB()
  values = (forumName,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM forum WHERE title LIKE %s;", values)

  myresult = mycursor.fetchall()
  forumList = []
  for x in myresult:
    artic = {
    "id":x[0],
    "title":x[1],
    "category":x[2],
    "location":x[3],
    "content":x[4],
    "imageURL":x[5],
    "likes":x[6],
    "Postedby":searchUserById(x[7])
    }



    forumList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return forumList



def getArticleName(articleName):
  mydb=defineDB()
  values = (articleName,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM articles WHERE name LIKE %s;", values)

  myresult = mycursor.fetchall()
  forumList = []
  for x in myresult:
    artic = {
    "id":x[0],
    "name":x[1],
    "description":x[2],
    "articleImageURL":x[3],
    "componentID":x[4],
    }



    forumList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return forumList


def getForumByCategory(cate):
  mydb=defineDB()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM forum WHERE category = %s ORDER BY id DESC",(cate,))

  myresult = mycursor.fetchall()
  forumList = []
  for x in myresult:
    artic = {
    "id":x[0],
    "title":x[1],
    "category":x[2],
    "location":x[3],
    "content":x[4],
    "imageURL":x[5],
    "likes":x[6],
    "Postedby":searchUserById(x[7])
    }

    forumList.append(artic)
  mycursor.close() 
  close_db_connection(mydb, "components")
  return forumList

def getForumById(desuwa):
  mydb=defineDB()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM forum WHERE id =%s ORDER BY id DESC",(desuwa,))

  myresult = mycursor.fetchall()
  forumList = []

  artic = {
    "id":myresult[0][0],
    "title":myresult[0][1],
    "category":myresult[0][2],
    "location":myresult[0][3],
    "content":myresult[0][4],
    "imageURL":myresult[0][5],
    "likes":myresult[0][6],
    "Postedby":searchUserById(myresult[0][7])
  }

  forumList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return forumList

def postForumtest(forum: ForumSchema):
  mydb=defineDB()
  anu=decode_user()
  email=anu["userID"]
  mycursor = mydb.cursor()
  values = (email,)
  mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
  myresult = mycursor.fetchall() 
  userId = myresult
  mycursor.close()
  close_db_connection(mydb, "components")
  return userId





def check_user(data: UserLoginSchema):
    mydb=defineDB()
    mycursor = mydb.cursor()

    email = data.email
    password = data.password
    res = (email,)

    mycursor.execute("SELECT * FROM users2 WHERE email= %s", res)
    myresult = mycursor.fetchall()
    mycursor.close()
    close_db_connection(mydb, "components")
    if (len(myresult) == 1):
        res_pass = myresult[0][3]
        if (password == res_pass):
            return True
    return False

def getCreden(data: UserLoginSchema):
    mydb=defineDB()
    if check_user(data):
        mycursor = mydb.cursor()
        email = data.email
        res = (email,)
        mycursor.execute("SELECT * FROM users2 WHERE email= %s", res)
        myresult = mycursor.fetchall()
        resId = myresult[0][0]
        resName = myresult[0][1]
        mycursor.close()
        close_db_connection(mydb, "components")
        return{
            "id":resId,
            "Username":resName
        }
    else:
        return{"error":"what the hell are you trying to do 🗿"}
 




def pushUser(data: UserSchema):
    mydb=defineDB()
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
        close_db_connection(mydb, "components")
        
        return False
    else:
        query = "insert into users2 (name, email, password) values (%s, %s, %s);" 
        res = (name,email,password)
        mycursor.execute(query, res)
        mydb.commit()
        mycursor.close()
        close_db_connection(mydb, "components")
        
        return True


def getbyId(id):
    mydb=defineDB()
    mycursor = mydb.cursor()

    # mycursor.execute("SELECT * FROM3 comps")
    res=(id,)
    mycursor.execute("SELECT * FROM comps WHERE id= %s", res)

    myresult = mycursor.fetchall()
    id=myresult[0][0]
    name=myresult[0][1]
    desc=myresult[0][2]
    example=myresult[0][3]
    
    myresult={
        "id":id,
        "name":name,
        "desc":desc,
        "example":example
    }
    mycursor.close()
    close_db_connection(mydb, "components")
    return myresult




def getArticlebyId(compid):
  mydb=defineDB()
  mycursor = mydb.cursor()
  res = (compid,)
  mycursor.execute("SELECT * FROM articles WHERE componentId= %s", res)
  myresult = mycursor.fetchall()
  articleList = []
  for t in myresult:
    artic = {
      "id":t[0],
      "name":t[1],
      "desc":t[2],
      "articleImageURL":t[3],
      "componentId":t[4]
    }
    articleList.append(artic)
  mycursor.close()
  close_db_connection(mydb, "components")
  return articleList


def getAllArticleby():
  mydb=defineDB()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM articles ORDER BY id DESC;")
  myresult = mycursor.fetchall()
  articleList = []
  for t in myresult:
    artic = {
      "id":t[0],
      "name":t[1],
      "desc":t[2],
      "articleImageURL":t[3],
      "componentId":t[4]
    }
    articleList.append(artic)
  mycursor.close() 
  close_db_connection(mydb, "components")
  return articleList

def getAllComponents():
  mydb=defineDB()
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM comps ORDER BY id DESC;")
  myresult = mycursor.fetchall()
  articleList = []
  for t in myresult:
    artic = {
      "id":t[0],
      "name":t[1],
      "desc":t[2],
      "imageExample":t[3],
    }
    articleList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return articleList

def getArticleID2(articleName):
  mydb=defineDB()
  values = (articleName,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM articles WHERE id=%s;", values)

  myresult = mycursor.fetchall()
  forumList = []
  for x in myresult:
    compID=(x[4],)
    mycursor2 = mydb.cursor() 
    mycursor2.execute("SELECT * FROM comps WHERE id=%s;", compID)
    myresult2 = mycursor2.fetchall()
    artic = {
    "id":x[0],
    "name":x[1],
    "description":x[2],
    "articleImageURL":x[3],
    "componentID":x[4],
    "componentName":myresult2[0][1]
    }
    
  
    forumList.append(artic)
  mycursor.close()
  mycursor2.close()
  close_db_connection(mydb, "components")
  return forumList

def postForum(forum: ForumSchema,email):
  mydb=defineDB()
  mycursor = mydb.cursor()
  values = (email,)
  mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
  myresult = mycursor.fetchall() 
  userId = myresult[0][0]
  lilcursorhehe = mydb.cursor()
  query = "insert into forum (title, category, location, content, imageUrl, userId) values (%s, %s, %s, %s, %s, %s);" 
  res = (forum.title, forum.category, forum.location, forum.content, forum.imageUrl,userId)
  lilcursorhehe.execute(query, res)
  mydb.commit()
  mycursor.close()
  lilcursorhehe.close()
  close_db_connection(mydb, "components")
  return {
    "error":"false",
    "message":"your post has been posted 😱🥶🥶🥶🥶🥶🥶🥶"
  }

def getCommentForum(forumid):
  mydb=defineDB()
  values = (forumid,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM comment WHERE forumID LIKE %s;", values)

  myresult = mycursor.fetchall()
  commentList = []
  for x in myresult:
    artic = {
    "id":x[0],
    "comment":x[1],
    "userID":x[2],
    "username":x[3],
    "replyFrom":x[4],
    "forumID":x[5]
    }



    commentList.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return commentList


def postComment(input: CommentSchema,email):
  mydb=defineDB()
  mycursor = mydb.cursor()
  values = (email,)
  mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
  myresult = mycursor.fetchall() 
  userId = myresult[0][0]
  username = myresult[0][1]
  lilcursorhehe = mydb.cursor()
  query = "insert into comment (comment, userID, username, replyFrom, forumID) values (%s, %s, %s, %s, %s);" 
  res = (input.comment, userId, username, 0 , input.forumID)
  lilcursorhehe.execute(query, res)
  mydb.commit()
  mycursor.close()
  lilcursorhehe.close()
  close_db_connection(mydb, "components")
  return {
    "error":"false",
    "message":"your comment has been posted 😱🥶🥶🥶🥶🥶🥶🥶",
    "commentInfo":{
        "Poster":username,
        "PosterID":userId,
        "forumID":input.forumID,
        "comment":input.comment
    }
  }


def replybyCommentID(input: ReplySchema,email):
  mydb=defineDB()
  mycursor = mydb.cursor()
  values = (email,)
  mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
  myresult = mycursor.fetchall() 
  userId = myresult[0][0]
  username = myresult[0][1]
  lilcursorhehe = mydb.cursor()
  query = "insert into comment (comment, userID, username, replyFrom, forumID) values (%s, %s, %s, %s, %s);" 
  res = (input.comment, userId, username, input.replyFrom , input.forumID)
  lilcursorhehe.execute(query, res)
  mydb.commit()
  mycursor.close()
  lilcursorhehe.close()
  close_db_connection(mydb, "components")
  return {
    "error":"false",
    "message":"your comment has been posted 😱🥶🥶🥶🥶🥶🥶🥶",
    "commentInfo":{
        "Poster":username,
        "PosterID":userId,
        "forumID":input.forumID,
        "comment":input.comment
    }
  }



def getSmallPartsComp(compid):
  mydb=defineDB()
  values = (compid,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM smallParts WHERE compID = %s;", values)

  myresult = mycursor.fetchall()
  smallParts = []
  for x in myresult:
    artic = {
    "id":x[0],
    "name":x[1],
    "description":x[2],
    "imageURL":x[3],
    "compID":x[4],
    }



    smallParts.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return smallParts

def getSmallPartsComp(id):
  mydb=defineDB()
  values = (id,)
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM smallParts WHERE id = %s;", values)

  myresult = mycursor.fetchall()
  smallParts = []
  for x in myresult:
    artic = {
    "id":x[0],
    "name":x[1],
    "description":x[2],
    "imageURL":x[3],
    "compID":x[4],
    }
    smallParts.append(artic) 
  mycursor.close()
  close_db_connection(mydb, "components")
  return smallParts


def postForum(forum: ForumSchema,email):
  mydb=defineDB()
  mycursor = mydb.cursor()
  values = (email,)
  mycursor.execute("SELECT * FROM users2 WHERE email= %s", values)
  myresult = mycursor.fetchall() 
  userId = myresult[0][0]
  lilcursorhehe = mydb.cursor()
  query = "insert into forum (title, category, location, content, imageUrl, userId) values (%s, %s, %s, %s, %s, %s);" 
  res = (forum.title, forum.category, forum.location, forum.content, forum.imageUrl,userId)
  lilcursorhehe.execute(query, res)
  mydb.commit()
  mycursor.close()
  lilcursorhehe.close()
  close_db_connection(mydb, "components")
  return {
    "error":"false",
    "message":"your post has been posted 😱🥶🥶🥶🥶🥶🥶🥶"
  }