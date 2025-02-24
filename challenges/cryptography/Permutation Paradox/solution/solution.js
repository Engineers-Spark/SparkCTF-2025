const jwt = require('jsonwebtoken');
const fs = require('fs');

// Load your public key (make sure the path is correct)
const publicKey = fs.readFileSync('./public.pem');

// Define your payload with role and expiration
const payload = {
    username: 'admin',
    role: 'admin', // Set role to admin
    exp: Math.floor(Date.now() / 1000) + (60 * 60) // Set expiration to 1 hour from now
};

// Sign the token
const token = jwt.sign(payload, publicKey, { algorithm: 'HS256', noTimestamp: true });

// Log the token
console.log(token);
