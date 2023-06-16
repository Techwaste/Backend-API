# Backend-API
Hiya! Gabriel here, this repo is for the backend of the app (ai model not included). Some of the features :  
- Auth
- Article
- Forum
- Image resizer
- Comment system

## how to use  
install the requirements
```bash
pip install -r requirements.txt
```
boot uvicorn
```bash
uvicorn main:app
```
or
```bash
python3 -m uvicorn main:app
```
ENV list
```
> PORT
> cres (service account for cloud storage)
> secret
> algorithm
> dbase
> duser
> dpw
> dip
```



# Api Documentation

### REGISTER

- URL
    
    /user/signup
    
- METHOD
    
    POST
    
- REQUEST BODY
```json
{
  "fullname": "string",
  "email": "user@example.com",
  "password": "string"
}
  ```  
- RESPONSE
    
```json
{
  "error": "false",
  "message": "User Created",
  "signupToken": {
    "access token": "aAiOiJfadsfdsafdsfKV1sadfQiLCfasdfdsaIUzIasdasdas32834hwytg90uerqhy908354nhg08erqh08q35nh0ierfh-ber-q9jh-945-0sdfjhme-tonjet9-tjn9-j-9j54h0-9nmeri0fhnbm-09rnobjknfds0ibn03n"
  }
}
```
    

### LOGIN

- URL
    
    /user/login
    
- METHOD
    
    POST
    
- REQUEST BODY
    
```json
{
  "email": "user@example.com",
  "password": "string"
}
```
    
- RESPONSE
```json
{
  "error": "false",
  "message": "login success",
  "loginResult": {
    "userId": {
      "id": 3,
      "Username": "gabrieltest3"
    },
    "token": {
      "access token": "eyJ0eXAiOiJKV1QiLCJhbGdF0TCem7fhAK57fIPyM3K9VI2I"
    }
  }
```
    

### PREDICT

- URL
    
    /predict
    
- METHOD
    
    POST
    
- HEADERS
    
    Content-Type: multipart/form-data
    
    Authorization: Bearer <Token>
    
- REQUEST BODY
    
    photo as file **`Image must be jpg, jpeg, or png format!`**
    
- RESPONSE
    
```json
{
  "compID": 2,
  "cable": 28.659623861312866
}
```
    

### COMPONENT

- URL
    
    /component{id}
    
- METHOD
    
    GET{id}
    
- HEADERS
    
    Authorization: Bearer <Token>
    
- PARAMETERS
name * = string
    
- RESPONSE
    
```json
{
  "error": "false",
  "message": "success",
  "componentList": {
    "id": 1,
    "name": "battery",
    "desc": "A battery consists of one or more electrochemical cells that contains chemical energy and release it as electrical energy. Batteries are generally safe if being used properly. The most common danger associated with batteries if mishandled or damaged is explosion or fire.",
    "example": "https://www.canford.co.uk/Images/ItemImages/large/59-104_01.jpg"
  }
}
```
    

### ARTICLE

- URL
    
    /article{id}
    
- METHOD
    
    GET{id}
    
- HEADERS
    
    Authorization: Bearer <Token>
    
- REQUEST BODY
    
    component id as STRING (foreign key from result-id)
    
- RESPONSE
    
```json
{
  "error": "false",
  "message": "success",
  "articleList": [
    {
      "id": 2,
      "name": "test3",
      "desc": "testing",
      "articleImageURL": "testing.test",
      "componentId": 3
    }
  ]
}
```
### Get All Article
- URL
    
    /allArticle
    
- METHOD
    
    GET
    
- HEADERS
    
    Authorization: Bearer <Token>
    
   
- RESPONSE
```json
{
  "error": "false",
  "message": "success",
  "componentList": [
    {
      "id": 6,
      "name": "nomer satu",
      "desc": "nomerSatu",
      "articleImageURL": "testing.test",
      "componentId": 1
    },
    {
      "id": 5,
      "name": "nomer satu",
      "desc": "nomerSatu",
      "articleImageURL": "testing.test",
      "componentId": 2
    },
    {
      "id": 4,
      "name": "nomer satu",
      "desc": "nomerSatu",
      "articleImageURL": "testing.test",
      "componentId": 2
    },
    {
      "id": 3,
      "name": "nomer satu",
      "desc": "nomerSatu",
      "articleImageURL": "testing.test",
      "componentId": 1
    },
    {
      "id": 2,
      "name": "test3",
      "desc": "testing",
      "articleImageURL": "testing.test",
      "componentId": 3
    },
    {
      "id": 1,
      "name": "test",
      "desc": "testing",
      "articleImageURL": "testing.test",
      "componentId": 1
    }
  ]
}
```

  
# Development notes
**DISCLAIMER:  some of the logs here are from my / past organization's api logs.** 
 

## Pre-release V-0.0.2
Pre-tested the like system  
changed the bucket destination  
removed auth requirements on component/{id} and article/{id}



## Release V-0.0.1
FINALLY I'M FREEEEEEEEEEEEEEE  
Updated .env   
Updated db query connection  
Removed collission between each db connections

<br><br>
## past development log  
vvvvvvv

## V-ALPHA 3
Added forum features, such as :  
- /forum/getall  
- /forum/id/{id}
- /forum/category/{category}
- /forum/title/{title}
- /forum/post
- /forum/upimagepost

Added comment features, such as :  
- /comments/post
- /comments/byforumid/{forumid}
- /reply/post  

![enter image description here](https://tenor.com/view/yui-gif-21788675.gif)

## V-ALPHA 2
I've tested the sql and stuff.  
the api has been deployed on cloud run.


## V-ALPHA 1
here me testing before making the api,
before that the sql relation will look like this :  
![enter image description here](https://cdn.discordapp.com/attachments/1023598916857499680/1106228887899357225/image.png)  
So we got 3 tables in total to make: users, article, comps
in article we have 5 parameters:

 1. idArticle {primary key}
 2. name
 3. description
 4. articleImageURL
 5. componentId {foreign key : from comps}

and in comps we have 4:

 1. id {primary key}
 2. name
 3. description
 4. imageExample

while image examples can be found and linked to google images, it will be more appropriate if we host those images ourselves. The images will be uploaded to bucket. I suppose 2 buckets would be enough, 1 for article, and the other one for comps.
the components will be consist of tons of components (obviously)  
['battery', 'cable', 'crt_tv', 'e_kettle', 'fridge', 'keyboard', 'laptop', 'light_bulb', 'monitor', 'mouse', 'pcb' , 'printer', 'rice_cooker', 'washing_machine' , 'phone']

the api docs can be found [here](https://github.com/w-capstone/API-docs)  
in this repo we will be testing some funcs before putting them all into apis.  
that's all  
stay comfy and remember :   
"life is a highway, I want ride it all night longgg~" - life is a highway, rascal flatts (from Cars)  
![enter image description here](https://media.tenor.com/LY9IxeF9UeUAAAAC/akari-akaza-yuri-yuri.gif)
