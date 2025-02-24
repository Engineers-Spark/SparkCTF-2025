const express   = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const app       = express();
const crypto    = require("crypto");
const bodyParser= require('body-parser')
const admin = require("./admin.js")
const { MongoClient } = require("mongodb");
const utils     = require('./utils.js');
const ObjectId  = require('mongodb').ObjectId ;
const axios = require('axios');
const mongoStore = require('connect-mongodb-session')(session);

const mongo_uri = process.env.MONGO_URI || 'mongodb://localhost:27017/todo'

const client = new MongoClient(mongo_uri);
const store = new mongoStore({
    collection: "userSessions",
    uri: mongo_uri,
    expires: 1000 * 60 * 60 * 24 * 365,
  });
const db = client.db("todo")

app.use(bodyParser.urlencoded({extended: true}));
app.use('/', express.static('public'))
app.use(cookieParser(crypto.randomBytes(128).toString("hex")))
app.set("view engine", "ejs");


app.use(session({
    secret: require("crypto").randomBytes(64).toString("hex"),
    store: store,
    saveUninitialized: false,
    resave: false,
    cookie: { 
        httpOnly: true,
        sameSite: "Lax",
        maxAge: 1000 * 60 * 60 * 24 * 365    
    }

}));


app.get('/', function(req, res) {
    return res.redirect("/dashboard")
});

app.get('/login', function(req, res) {
    return res.render("login",{"status":""});
});

app.get('/logout', function(req, res) {
    if (req.session) {
        req.session.destroy(err => {
          if (err) {
            return res.status(400).send('Something went wrong')
          } else {
            return res.redirect('/login')
          }
        });
      } else {
        return res.end()
      }
});

app.post('/login', function(req, res) {
    let { username, password } = req.body;
    
    if (username && typeof username == "string" && password && typeof password == "string") {
        db.collection("users").findOne({ username:username,password:password}).then((user) => {
		if (user) {
        		req.session.loggedIn = true
	            	req.session.username = user.username
        		return res.redirect('/dashboard')
        	} else {
	    		return res.render("login",{"status":"Invalid login!"});
		}
       }).catch((e) => res.render("login",{"status":e.toString()}))
    }else{
        return res.render("login",{"status":"bad!"});
    }
});

app.get('/dashboard', utils.authcheck, async function(req, res, next) {
        let username = req.session.username
        if (username) {
                notes = await db.collection("notes").find({owner:username}).toArray()
                if (notes){
                    return res.render("dashboard",{"username":username,"notes":notes})
                }else{
                    return res.render("dashboard",{"username":username,"notes":0})
                }
            }
        
});


app.get("/note/:id", async function(req, res) {
    let id = req.params.id;
    if (!id && typeof id != "string") {
        return res.send("Not found")
    }
    try {
        if (utils.isValidObjectId(id)){
            note = await db.collection("notes").findOne({_id:new ObjectId (id)})
        }else{
            note = await db.collection("notes").findOne({_id:id})
        }
        
        if (note){
            return res.render("note",{"note":note})
        }else{
            return res.send("Not found")
        }    
    } catch (e) {
        return res.send("Not found")
    }
});

// TODO: finish the api properly..
app.get('/api/notes', async function(req, res) {

    try {
        notes = await db.collection("notes").find({protected:0}).toArray()
        if (notes){
            return res.json(notes)
        }else{
            return res.send("Not found")
        }    
    } catch (e) {
        return res.send("Not found")
    }
});


app.get('/api/search', async function(req, res) {

    if (req.connection.remoteAddress != "127.0.0.1") {
        return res.status(403).send("No! Only for localhost")
    }

    let input = req.query.input;
    const input_regex =  /^[a-zA-Z0-9_{ }]+$/;
    
    if (!input && typeof input != "string") {
        return res.send("Nope")
    }
    
    if (!input.match(input_regex)){
        return res.send("nah")
    }

    try {
        // get the note starting with input
        note = await db.collection("notes").findOne({ content: { $regex: "^"+input }})
        if (note){
            return res.render("search",{"note":note})
        }else{
            return res.json({"Error":"Not found"})
        }    
    } catch (e) {
        return res.json({"Error":"Error"})
    }
});


app.get("/report", utils.authcheck, (req, res) => {
    var url = req.query.url;
    var client_response = req.query["h-captcha-response"]
    var data = {
        response: client_response,
        secret: process.env.CAPTCHA_SECRET || "0x0000000000000000000000000000000000000000"
    };

    const ex = /(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})/gi
    if (url) {
        
        axios.post('https://api.hcaptcha.com/siteverify', data, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            })
            .then(function(result) {
                if (result.data.success) {
                    if (url.match(ex)) {
                        admin.visit(url).then((e) => {
                            return res.render("report", {
                                "result": "Visited successfully"
                            });
                        }).catch((err) => {
                            console.log(err)
                            return res.render("report", {
                                "result": "Something went wrong.."
                            });
                        });
                    } else {
                        return res.render("report", {
                            "result": "Invalid URL"
                        });
                    }
                } else {
                    return res.render("report", {
                        "result": "Invalid Captcha!"
                    });
                }
            })
            .catch(function(err) {
                console.log(err)
                return res.render("report", {
                    "result": "Invalid Captcha!"
                });
            });

    } else {
        return res.render("report", {
            "result": ""
        });
    }
})

app.listen(3000, "0.0.0.0", () => {
    console.log(`Server Running at 127.0.0.1:3000`);
});
