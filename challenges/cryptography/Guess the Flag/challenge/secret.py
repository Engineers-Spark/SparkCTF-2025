import random
import time
import os

seed = (str(random.randint(10,99)) +((hex(int(time.time()))[4:])))
f = b"30ead4950a9148d7f2c0352262dce642"
FLAG = b"SparkCTF{" + f[:12] + seed.encode() + f[-12:] +b"}"
