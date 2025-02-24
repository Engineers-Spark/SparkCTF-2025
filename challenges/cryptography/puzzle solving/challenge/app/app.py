from flask import Flask, render_template, request, redirect, url_for, make_response, g
from datetime import datetime, timedelta
from functools import wraps
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
from secret import FLAG, KEY

def encrypt_ecb(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(data.encode(), 16))

def decrypt_ecb(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), 16).decode()

def get_payload(json):
    return "&".join([f"{k}={v}" for k, v in json.items()]).strip()

def parse(payload):
    return dict([p.split("=") for p in payload.split("&")])


app = Flask(__name__)

USER = "spark"
PASS = "password"

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            token = request.cookies.get('token')
            if not token:
                return "<h1>Unauthorized access! Please log in.</h1>"
            try:
                decrypted = decrypt_ecb(bytes.fromhex(token), KEY)
                decrypted = dict([p.split("=") for p in decrypted.split("&")])
                g.user = decrypted['username']
                g.role = decrypted['role']
                if role and g.role != role:
                    return "<h1>Unauthorized access! Admins only.</h1>"
            except Exception as e:
                return "<h1>Invalid token! Please log in.</h1>"
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    gmail = request.form['email']
    if "@" not in gmail:
        return "<h1>Invalid email.</h1>"
    if username == USER and password == PASS:
        json = {
            "email": gmail,
            'username': username,
            "role": "player",
        }
        if "&=" in str(json):
            return "<h1>Invalid input.</h1>"
        payload = get_payload(json)
        token = encrypt_ecb(payload, KEY).hex()
        resp = make_response(redirect(url_for('dashboard')))
        resp.set_cookie('token', token, httponly=True, samesite='Strict')
        return resp
    return "<h1>Invalid Credentials. Please try again.</h1>"

@app.route('/dashboard')
@token_required()
def dashboard():
    return f"<h1>Welcome to your dashboard, {g.user}! Your role is: {g.role}.</h1>"

@app.route('/admin')
@token_required(role='admin')
def admin():
    return "<h1>Welcome to the admin page!</h1>\n" + FLAG

@app.route('/logout')
def logout():
    resp = make_response("<h1>You have been logged out.</h1>")
    resp.delete_cookie('token')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6200)