import os
import glob
import ruamel.yaml
import ruamel.yaml.util
from argparse import ArgumentParser

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=4, sequence=6, offset=3)
categories = ["web", "cryptography", "forensics", "pwn", "rev", "blockchain", "hardware"]

with open("waves.yml", 'r') as stream:
    waves = yaml.load(stream)

def init_challenges():
    for category in categories:
        if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
            challenges = glob.glob(f"../../SparkCTF-2025-dev/challenges/{category}/*")
            for challenge in challenges:
                chal = os.path.basename(challenge)
                if chal == 'test-challenge':
                    continue
                else:
                    print(f"[+] Installing challenge: {challenge}")
                    os.system(f"ctf challenge add \"{challenge}\" && ctf challenge install \"{challenge}\"")
        else:
            print(f"[-] Can't find: {category}")
            exit(1)
    exit(0)


def sync_verify():
    for category in categories:
        if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
            challenges = glob.glob(f"../../SparkCTF-2025-dev/challenges/{category}/*")
            for challenge in challenges:
                chal = os.path.basename(challenge)
                if chal == 'test-challenge':
                    continue
                else:
                    print(f"[+] Syncing challenge: {chal}")
                    os.system(f"ctf challenge sync \"{challenge}\" && ctf challenge verify \"{challenge}\"")
        else:
            print(f"[-] Can't find: {category}")
            exit(1)
    exit(0)


def reverse_sync_verify():
    for category in categories:
        if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
            challenges = glob.glob(f"../../SparkCTF-2025-dev/challenges/{category}/*")
            for challenge in challenges:
                chal = os.path.basename(challenge)
                if chal == 'test-challenge':
                    continue
                else:
                    print(f"[+] Reverse Syncing challenge: {chal}")
                    os.system(f"ctf challenge mirror \"{challenge}\" && ctf challenge verify \"{challenge}\"")
        else:
            print(f"[-] Can't find: {category}")
            exit(1)
    exit(0)


def activate(category, chall):
    if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
        with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'r') as stream:
            challenge_config = yaml.load(stream)        
        if challenge_config['state'].lower().strip() == 'visible':
            warn = input("[!] this challenge is already visible, are you sure you wanna continue? (y/n): ")
            if warn.lower().strip() == 'y':
                challenge_config['state'] = 'visible'
                with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'w') as stream:
                    yaml.dump(challenge_config, stream)
                print(f"[+] challenge {chall} is now visible!")
        else:
            challenge_config['state'] = 'visible'
            with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'w') as stream:
                yaml.dump(challenge_config, stream)
            print(f"[+] challenge {chall} is now visible!")
    else:
        print(f"[-] Cant find category: {category}")


def start_wave(id):
    id = int(id)
    print(f"[+] Activating wave {str(id)} challenges:\n")
    w_ = waves[id]
    for category in w_:
        if w_[category]:
            for chall in w_[category]:
                if chall:
                    print(f"=> challenge: {category} - {chall}")
                    activate(category,chall)
    sync_verify()

def hide(category, chall):
    if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
        with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'r') as stream:
            challenge_config = yaml.load(stream)        
        if challenge_config['state'].lower().strip() == 'hidden':
            warn = input("[!] this challenge is already hidden, are you sure you wanna continue? (y/n): ")
            if warn.lower().strip() == 'y':
                challenge_config['state'] = 'hidden'
                with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'w') as stream:
                    yaml.dump(challenge_config, stream)
                print(f"[+] challenge {chall} is now hidden!")
        else:
            challenge_config['state'] = 'hidden'
            with open(f"../../SparkCTF-2025-dev/challenges/{category}/{chall}/challenge.yml", 'w') as stream:
                yaml.dump(challenge_config, stream)
            print(f"[+] challenge {chall} is now hidden!")
    else:
        print(f"[-] Cant find category: {category}")

def hide_wave(id):
    id = int(id)
    print(f"[+] Hiding wave {str(id)} challenges:\n")
    w_ = waves[id]
    for category in w_:
        if w_[category]:
            for chall in w_[category]:
                if chall:
                    print(f"=> challenge: {category} - {chall}")
                    hide(category,chall)
    sync_verify()


def activate_all():
    for category in categories:
        if os.path.exists(f"../../SparkCTF-2025-dev/challenges/{category}"):
            challenges = glob.glob(f"../../SparkCTF-2025-dev/challenges/{category}/*")
            for chall in challenges:            
                with open(f"{chall}/challenge.yml", 'r') as stream:
                    challenge_config = yaml.load(stream)        
                if challenge_config['state'].lower().strip() == 'visible':
                    warn = input("[!] this challenge is already visible, are you sure you wanna continue? (y/n): ")
                    if warn.lower().strip() == 'y':
                        challenge_config['state'] = 'visible'
                        with open(f"{chall}/challenge.yml", 'w') as stream:
                            yaml.dump(challenge_config, stream)
                        print(f"[+] challenge {chall} is now visible!")
                else:
                    challenge_config['state'] = 'visible'
                    with open(f"{chall}/challenge.yml", 'w') as stream:
                        yaml.dump(challenge_config, stream)
                    print(f"[+] challenge {chall} is now visible!")
        else:
            print(f"[-] Cant find category: {category}")
    sync_verify()

parser = ArgumentParser()
parser.add_argument('--init', action='store_true', help="Initialize challenges")
parser.add_argument('--sync', action='store_true', help="Sync and verify challenges from local to instance")
parser.add_argument('--reverse-sync', action='store_true', help="Sync and verify challenges from CTFd to local")    
parser.add_argument('--activate-wave', type=str, help=" Activate specific wave challenges")
parser.add_argument('--hide-wave', type=str, help=" Hide specific wave challenges")
parser.add_argument('--activate-all',action='store_true', help=" Activate all challenges")

args = parser.parse_args()

if args.init:
    init_challenges()
elif args.sync:
    sync_verify()
elif args.reverse_sync:
    reverse_sync_verify()    
elif args.activate_wave:
    start_wave(args.activate_wave)
elif args.hide_wave:
    hide_wave(args.hide_wave)   
elif args.activate_all:
    activate_all() 
else:
    print("[-] No valid argument provided")
