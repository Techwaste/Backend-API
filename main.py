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

use_env = os.environ.get("USE_ENV")

if use_env != "True":
    load_dotenv()
    key_pi = os.getenv("SA_JSON")
else:
    key_pi = os.environ.get("SA_JSON")

# GOOGLE_APPLICATION_CREDENTIALS = key_pi
with open("service_account.json", "w") as file:
    file.write(key_pi)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service_account.json"
form = str(random.randint(3, 3265792139879102375))
bucketName = "techwaste"


def storage_thingy(blobName, filePath, bucketName):
    storageClient = storage.Client()
    dir(storageClient)
    bucket = storageClient.bucket(bucketName)
    vars(bucket)
    bucket = storageClient.get_bucket(bucketName)
    blob = bucket.blob(blobName)
    blob.upload_from_filename(filePath)

    return blob


token = []


async def testcoded(request: Request):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    return decode_user(token2)


def decode_user(token2):
    decoded_data = jwt.decode(token2, JWT_SECRET, JWT_ALGORITHM)
    return decoded_data


posts = [
    {
        "id": 1,
        "title": "rent-a-gf",
        "text": "stupid *ss anime only psychopath watch this"

    },
    {
        "id": 2,
        "title": "kimi-no-nawa",
        "text": "overrated but ok"

    },
    {
        "id": 3,
        "title": "demon-slayer",
        "text": "overrated af and also it's the equivalent of fortnite in anime industry (only 5 yolds love it)"

    }


]


users = []

app = FastAPI()


# Get test
@app.get("/", tags=["test"])
def greet():
    return {"YAHOOOOO~!": "THE PROPECHY STIGNEAS!"}


# Get posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}

# get single post by id


@app.get("/post/{id}", tags=["posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {
            "error": "erm, there is no post..."
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.get("/component/{id}", tags=["components"])
def comps(id: str):
    result = getbyId(id)
    return {
        "error": "false",
        "message": "success",
        "componentList": result
    }


@app.get("/article/{id}", tags=["articles"])
def artic(compid: str):
    result = getArticlebyId(compid)
    return {
        "error": "false",
        "message": "success",
        "articleList": result
    }


@app.get("/allArticle", tags=["articles"])
def compsed():
    result = getAllArticleby()
    return {
        "error": "false",
        "message": "success",
        "componentList": result
    }


# Post new post
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post: PostSchema):
    post.id = len(posts)+1
    posts.append(post.dict())
    return {
        "info": "degenericity added"
    }

# User thingy I forgor basically
# @app.post("/user/signup", tags=["user"])
# def user_signup(user : UserSchema = Body(...)):
#    users.append(user)
#    return signJWT(user.email)


@app.post("/user/signup", tags=["user"])
def user_signup(user: UserSchema = Body(...)):
    users.append(user)

    if pushUser(user):
        return {
            "error": "false",
            "message": "User Created",
            "signupToken": signJWT(user.email)
        }
    else:
        return {
            "error": "true",
            "message": "Email already taken 🗿"
        }


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        token.clear()
        nanikore = signJWT(user.email)
        token.append(nanikore)
        return {
            "error": "false",
            "message": "login success",
            "loginResult": {
                "userId": getCreden(user),
                "token": nanikore,
            }}

    else:
        return {
            "error": "true",
            "message": "Invalid login details! 🗿"
        }


async def testcoded(request: Request):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    return {"hasil": token2,
            "test-token": decode_user(token2)}


@app.get("/meneh", dependencies=[Depends(jwtBearer())], tags=["test"])
def coba():
    wibu = decode_user()
    email = wibu["userID"]
    return email


@app.post("/forum/postest", dependencies=[Depends(jwtBearer())], tags=["forum"])
def posting(forum: ForumSchema = Body(...)):
    return postForumtest(forum)


@app.get("/forum/getall", tags=["forum"])
def forumGetAll():

    forum = getAllForum()
    if (forum):
        return {
            "error": "false",
            "message": "success",
            "forum": forum
        }
    else:
        return {
            "error": "true",
            "message": "it's either no forum or you wanna do something terrible 💀"
        }


@app.get("/forum/id/{id}", dependencies=[Depends(jwtBearer())], tags=["forum"])
def forid(id):
    result = getForumById(id)
    if (result):
        return {
            "error": "false",
            "message": "success",
            "forum": result
        }
    else:
        return {
            "error": "true",
            "message": "are you serious rait now braw 💀"
        }


@app.get("/forum/category/{category}", dependencies=[Depends(jwtBearer())], tags=["forum"])
def forumCategory(category):
    forum = getForumByCategory(category)
    if (forum):
        return {
            "error": "false",
            "message": "success",
            "forum": forum
        }
    else:
        return {
            "error": "true",
            "message": "it's either there's no forum for this category or you wanna do something terrible 💀"
        }


@app.get("/decode/", dependencies=[Depends(jwtBearer())], tags=["decode"])
async def testcoded(request: Request):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    jsonResponse = decode_user(token2)
    print(jsonResponse)
    return (jsonResponse["userID"])


@app.get("/components/", tags=["components"])
def getAllComp():
    output = getAllComponents()
    if (output):
        return {
            "error": "false",
            "message": "success",
            "components": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.get("/forum/title/{title}", tags=["forum"])
def getForumbyName(title):
    output = getForumName(title)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "Forum": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.get("/article/name/{name}", tags=["articles"])
def getArticlebyName(name):
    output = getArticleName(name)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "article": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.get("/article/id/{id}", tags=["articles"])
def getArticlebyName(id):
    output = getArticleID2(id)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "article": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.post("/forum/post", dependencies=[Depends(jwtBearer())], tags=["forum"])
def posting(request: Request, forum: ForumSchema = Body(...)):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    jsonResponse = decode_user(token2)
    email = jsonResponse["userID"]

    postForum(forum, email)
    if (forum):
        return {
            "error": "false",
            "message": "your post has been posted 😱🥶🥶🥶🥶🥶🥶🥶"

        }
    else:
        return {
            "error": "true",
            "message": "what are you trying to do lil bro 💀"

        }


@app.post("/comments/post", dependencies=[Depends(jwtBearer())], tags=["comments"])
def postComments(request: Request, post: CommentSchema = Body(...)):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    jsonResponse = decode_user(token2)
    email = jsonResponse["userID"]
    if (post):
        return postComment(post, email)


@app.get("/comments/byforumid/{forumid}", tags=["comments"])
def getCommentsbyForumId(forumid):
    output = getCommentForum(forumid)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "article": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.post("/reply/post", dependencies=[Depends(jwtBearer())], tags=["comments"])
def replyCommentID(request: Request, post: ReplySchema = Body(...)):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]
    jsonResponse = decode_user(token2)
    email = jsonResponse["userID"]
    if (post):
        return replybyCommentID(post, email)


@app.get("/smallparts/bycompid/{compid}", tags=["components"])
def getsmallpartsbycompid(compid):
    output = getSmallPartsComp(compid)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "smallParts": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.get("/smallparts/byid/{id}", tags=["components"])
def getsmallpartsbycompid(id):
    output = getSmallPartsComp(id)
    if (output):
        return {
            "error": "false",
            "message": "success",
            "smallParts": output
        }
    else:
        return {
            "error": "true",
            "message": "waduh kenapa nih bang?"
        }


@app.post("/forum/upimagepost", dependencies=[Depends(jwtBearer())], tags=["forum"])
async def posting(request: Request, file: UploadFile = File(...)):
    authorization_header = request.headers["Authorization"]
    token2 = authorization_header.split(" ")[1]

    savedForm = form
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg, jpeg, or png format!"
    contents = await file.read()

    image = Image.open(io.BytesIO(contents))
    image.save(file.filename)

    storage_thingy("savedUser/"+"image"+savedForm+"USED" +
                   token2, file.filename, bucketName)
    saved = "https://storage.googleapis.com/techwaste/savedUser/" + \
        "image"+savedForm+"USED"+token2
    os.remove(file.filename)

    if (saved):
        return {
            "error": "false",
            "message": "your image has been posted 😱🥶🥶🥶🥶🥶🥶🥶",
            "imgURL": saved

        }
    else:
        return {
            "error": "true",
            "message": "what are you trying to do lil bro 💀"

        }

# #don't worry about this one
# @app.get("/resize",tags=["image"])
# async def resize_image(file: UploadFile = File(...), width: int = 300, height: int = 300):
#     # Read the uploaded image file
#     image = Image.open(BytesIO(await file.read()))

#     # Resize the image
#     resized_image = image.resize((width, height))

#     # Save the resized image to disk
#     output_path = "resized_image.jpg"  # Specify the desired output file path
#     resized_image.save(output_path, format="JPEG")

#     return {"message": "Image resized and saved successfully.", "file_path": output_path}


@app.get("/resize/imageurl", tags=["image"])
async def resize_image(
    image_url: str = "https://storage.googleapis.com/somethingssss/PXL_20230203_102403556.jpg",
    width: int = 300,
    height: int = 300
):
    # Fetch the image from the provided URL
    response = requests.get(image_url)
    response.raise_for_status()

    # Read the fetched image
    image = Image.open(BytesIO(response.content))

    # Resize the image
    resized_image = image.resize((width, height))

    # Save the resized image to disk
    output_path = "resized_image.jpg"  # Specify the desired output file path
    resized_image.save(output_path, format="JPEG")

    # return {"message": "Image resized and saved successfully.", "file_path": output_path}
    return FileResponse(output_path)


@app.get("/crop/imageurl", tags=["image"])
async def crop_image(
    image_url: str = "https://storage.googleapis.com/somethingssss/PXL_20230203_102403556.jpg",
    width: int = 300,
    height: int = 300
):
    # Fetch the image from the provided URL
    response = requests.get(image_url)
    response.raise_for_status()

    # Open the fetched image using PIL
    image = Image.open(BytesIO(response.content))

    # Calculate the aspect ratio of the original image
    aspect_ratio = image.width / image.height

    # Calculate the target width based on the desired height and aspect ratio
    target_width = int(height * aspect_ratio)

    # Resize the image while maintaining the aspect ratio
    resized_image = image.resize((target_width, height))

    # Calculate the cropping coordinates to remove the extra height
    left = 0
    top = (resized_image.height - height) / 2
    right = left + width
    bottom = top + height

    # Crop the image to the desired width and height
    cropped_image = resized_image.crop((left, top, right, bottom))

    # Save the cropped image to a BytesIO buffer
    output_path = "resized_image.jpg"
    cropped_image.save(output_path, "JPEG")

    # Return the image as a response
    return FileResponse(output_path)


@app.get("/crop2/imageurl", tags=["image"])
async def crop_image2(
    image_url: str = "https://storage.googleapis.com/somethingssss/PXL_20230203_102403556.jpg",
    width: int = 300,
    height: int = 300
):
    # Fetch the image from the provided URL
    response = requests.get(image_url)
    response.raise_for_status()

    # Open the fetched image using PIL
    image = Image.open(BytesIO(response.content))

    # Calculate the desired aspect ratio
    aspect_ratio = width / height

    # Calculate the actual aspect ratio of the original image
    original_aspect_ratio = image.width / image.height

    # Resize the image while maintaining the correct aspect ratio
    if original_aspect_ratio > aspect_ratio:
        new_width = int(height * original_aspect_ratio)
        resized_image = image.resize((new_width, height))
    else:
        new_height = int(width / original_aspect_ratio)
        resized_image = image.resize((width, new_height))

    # Create a blank white canvas with the specified dimensions
    canvas = Image.new("RGB", (width, height), "white")

    # Paste the resized image onto the canvas
    offset = ((width - resized_image.width) // 2,
              (height - resized_image.height) // 2)
    canvas.paste(resized_image, offset)

    # Save the canvas to a BytesIO buffer
    # image_buffer = BytesIO()
    output_path = "resized_image.jpg"
    canvas.save(output_path, "JPEG")

    # Return the image as a response
    return FileResponse(output_path)


if __name__ == "__main__":
    import uvicorn
