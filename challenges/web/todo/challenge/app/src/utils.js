const { ObjectId } = require('mongodb');

module.exports = {  
    authcheck: function(req, res, next) {
        if (!req.session.loggedIn){
            res.redirect('/login')
        }
        next()   
    },
    admin_authcheck: function(req, res, next) {
        if (req.session.loggedIn && req.session.username === "admin@spark.tech"){
            next()
        }else{
            res.redirect('/dashboard')
        }
    },
    isValidObjectId: function(id) {
        return ObjectId.isValid(id) && (new ObjectId(id)).toString() === id;
    }
  }
