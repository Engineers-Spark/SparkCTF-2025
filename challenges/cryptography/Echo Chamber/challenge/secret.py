import random
import time
import os
seed = (str(random.randint(10,99)) +((hex(int(time.time()))[4:])))
f = b"5f94de56dd6bc52a21df89fda5d64f4f"
FLAG = b"SparkCTF{" + f[:12] + seed.encode() + f[-12:] +b"}"
KEY = os.urandom(16)
