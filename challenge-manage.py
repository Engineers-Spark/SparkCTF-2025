import os
import glob
from argparse import ArgumentParser

categories = ["web", "cryptography", "pwn"]

tcp = ["The Notorious liB.I.C","hashing stuff", "tajin","Guess The Flag", "Echo Chamber", "Hash Overdrive", "roller", "www", "retro"]
http = ["todo", "BugReportGen", "capitalism", "puzzle solving", "Permutation Paradox"]

def start(category):
    if os.path.exists(f"challenges/{category}"):
        challenges = glob.glob(f"challenges/{category}/*")
        for challenge_path in challenges:
            chal = os.path.basename(challenge_path)
            if chal == 'test-challenge':
                continue
            else:
                print(f"[+] {category} - Starting challenge: {chal}")
                os.system(f"docker compose \-f \"{challenge_path}/docker-compose.yml\" up \-d")
    else:
        print(f"[-] Can't find: {category}")
        exit(1)
    exit(0)


def stop(category):
    if os.path.exists(f"challenges/{category}"):
        challenges = glob.glob(f"challenges/{category}/*")
        for challenge_path in challenges:
            chal = os.path.basename(challenge_path)
            if chal == 'test-challenge':
                continue
            else:
                print(f"[+] {category} - Starting challenge: {chal}")
                os.system(f"docker compose \-f \"{challenge_path}/docker-compose.yml\" down ")
    else:
        print(f"[-] Can't find: {category}")
        exit(1)
    exit(0)


def start_tcp():
    for category in categories:
        if os.path.exists(f"challenges/{category}"):
            challenges = glob.glob(f"challenges/{category}/*")
            for challenge_path in challenges:
                chal = os.path.basename(challenge_path)
                if chal in tcp:
                    print(f"[+] {category} - Starting challenge: {chal}")
                    os.system(f"docker compose \-f \"{challenge_path}/docker-compose.yml\" up -d")
        else:
            print(f"[-] Can't find: {category}")

def stop_tcp():
    for category in categories:
        if os.path.exists(f"challenges/{category}"):
            challenges = glob.glob(f"challenges/{category}/*")
            for challenge_path in challenges:
                chal = os.path.basename(challenge_path)
                if chal in tcp:
                    print(f"[+] {category} - Stopping challenge: {chal}")
                    os.system(f"cd \"{challenge_path}\"; docker compose down ")
        else:
            print(f"[-] Can't find: {category}")


def start_http():
    for category in categories:
        if os.path.exists(f"challenges/{category}"):
            challenges = glob.glob(f"challenges/{category}/*")
            for challenge_path in challenges:
                chal = os.path.basename(challenge_path)
                if chal in http:
                    print(f"[+] {category} - Starting challenge: {chal}")
                    os.system(f"docker compose \-f \"{challenge_path}/docker-compose.yml\" up -d")
        else:
            print(f"[-] Can't find: {category}")

def stop_http():
    for category in categories:
        if os.path.exists(f"challenges/{category}"):
            challenges = glob.glob(f"challenges/{category}/*")
            for challenge_path in challenges:
                chal = os.path.basename(challenge_path)
                if chal in http:
                    print(f"[+] {category} - Stopping challenge: {chal}")
                    os.system(f"cd \"{challenge_path}\"; docker compose down ")
        else:
            print(f"[-] Can't find: {category}")

parser = ArgumentParser()
parser.add_argument('--start', help="Start challenges from a category")
parser.add_argument('--stop', help="Stop challenges from a category")
parser.add_argument('--tcp', help="start or stop tcp challenges")
parser.add_argument('--http', help="start or stop http challenges")
args = parser.parse_args()

if args.start:
    category = args.start
    start(category)
elif args.stop:
    category = args.stop
    stop(category)
elif args.tcp:
    t = args.tcp.strip().lower()
    if t in ["stop","start"]:
        if t == "start":
            start_tcp()
        if t == "stop":
            stop_tcp() 
elif args.http:
    h = args.http.strip().lower()
    if h in ["stop","start"]:
        if h == "start":
            start_http()
        if h == "stop":
            stop_http()                        
else:
    print("[-] No valid argument provided")
