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
