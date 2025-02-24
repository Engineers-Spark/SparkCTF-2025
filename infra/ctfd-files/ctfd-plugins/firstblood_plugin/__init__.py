import requests
import re
import json
from CTFd.utils.scores import get_team_standings
from flask import request
from flask.wrappers import Response
from CTFd.utils.dates import ctftime
from CTFd.models import Challenges, Solves, Teams
from CTFd.utils import config as ctfd_config
from CTFd.utils.user import get_current_team, get_current_user
from functools import wraps
from CTFd.models import Teams
from .conf import WEBHOOK,TOKEN,BLOOD_DISCORD_WEBHOOK,UPDATES_DISCORD_WEBHOOK
from discord_webhook import DiscordWebhook, DiscordEmbed
import glob, random

sanreg = re.compile(r'(~|!|@|#|\$|%|\^|&|\*|\(|\)|\_|\+|\`|-|=|\[|\]|;|\'|,|\.|\/|\{|\}|\||:|"|<|>|\?)')
sanitize = lambda m: sanreg.sub(r"\1", m)

def send(url, data):
    d = json.dumps(data,default=str)
    requests.post(url,data=d,headers={"Content-Type": "application/json", "Verify-CTFd": TOKEN})

def random_gif():
    gifs = glob.glob("./CTFd/plugins/firstblood_plugin/images/*.gif")
    r_gif = random.choice(gifs)
    return r_gif

def discord_notif(title,content):
  
    webhook = DiscordWebhook(url=UPDATES_DISCORD_WEBHOOK)
    embed = DiscordEmbed(title=f"{title}",description=f"@everyone {content}",color="237feb")
    embed.set_timestamp()   
    webhook.add_embed(embed)       
    webhook.execute()

def discord_update(notification):
    webhook = DiscordWebhook(UPDATES_DISCORD_WEBHOOK)
    embed = DiscordEmbed(title="UPDATE 🔔",description=f"{notification}")
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()

def discord_blood(team,challenge):
    webhook = DiscordWebhook(BLOOD_DISCORD_WEBHOOK)
    embed = DiscordEmbed(title="FIRST BLOOD 🩸",description=f"Team **{team}** just got the first blood on challenge **{challenge}** !!",color="e74c3c")
    embed.set_timestamp()
    image = random_gif()
    with open(image, "rb") as f:
        filename = image.split('/')[-1]
        webhook.add_file(file=f.read(), filename=filename)

    embed.set_thumbnail(url="attachment://"+filename)
    webhook.add_embed(embed)
    webhook.execute()

def load(app):
    TEAMS_MODE = ctfd_config.is_teams_mode()
    if WEBHOOK:
        try:
            requests.get(WEBHOOK)
        except:
            print("\n***LIVESCOREBOARD WARNING:WEBHOOK NOT WORKING! Plugin disabled***\n")
            return
    else:
        print("\n***LIVESCOREBOARD WARNING:WEBHOOK NOT SET! Plugin disabled***\n")
        return

    def challenge_attempt_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not ctftime():
                return result
            if isinstance(result, Response):
                data = result.json
                if (isinstance(data, dict) and data.get("success") == True and isinstance(data.get("data"), dict)and data.get("data").get("status") == "correct"):
                    if request.content_type != "application/json":
                        request_data = request.form
                    else:
                        request_data = request.get_json()

                    
                    first_blood = 0 
                    challenge_id = request_data.get("challenge_id")
                    challenge = Challenges.query.filter_by(id=challenge_id).first_or_404()
                    # get all solves for that challenge
                    solvers = Solves.query.filter_by(challenge_id=challenge.id)
                    
                    if TEAMS_MODE: 
                        solvers = solvers.filter(Solves.team.has(hidden=False))
                    
                    # if solve count for the challenge is 1 => firstblooded
                    # check if first blood
                    num_solves_chall = solvers.count()
                    if num_solves_chall - 1 == 0: 
                        first_blood = 1
            
                    # get team / user details
                    team = get_current_team()
                    user = get_current_user()

                    # if team hidden dont send anything
                    if team.hidden:
                        return result

                    # get current submission
                    submission = Solves.query.filter_by(account_id=user.account_id, challenge_id=challenge_id).first()
                    solve_details = [{
                        "team": sanitize("" if team is None else team.name),
                        "user": sanitize(user.name),
                        "challenge": sanitize(challenge.name),
                        "first_blood": first_blood,
                        "date": str(submission.date)
                    }]

                    score = get_team_standings()
                    score_result = format_scoreboard(score)

                    # send firstbloods to discord webhook
                    if first_blood and BLOOD_DISCORD_WEBHOOK != "":
                        try:
                            discord_blood(sanitize("" if team is None else team.name),sanitize(challenge.name))
                        except Exception as err:
                            print("Something went wrong with discord webhook..\n"+err)
                            
                    # send solve
                    send(WEBHOOK + "/api/solve", solve_details)
                    # send scoreboard
                    send(WEBHOOK + "/api/scoreboard", score_result)

            return result
        return wrapper

    def format_scoreboard(data):
        scoreboard = []
        for index, item in enumerate(data):
            team = Teams.query.filter_by(name=item[2]).first()
            solves = team.get_solves()
            team_score = {
                "team": sanitize(item[2]),
                "score": item[3],
                "num_solves": len(solves)
            }
            scoreboard.append(team_score)

        return scoreboard
    
    def notification_detect(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if not ctftime():
                return result
            if isinstance(result, Response):
                data = result.json
                if isinstance(data, dict) and data.get("success") == True and isinstance(data.get("data"), dict):
                    notification = data.get("data")
                    title = notification.get('title')
                    content = notification.get('content')
                    date = notification.get('date')
                    discord_notif(title,content)
            return result
        return wrapper

    

    app.view_functions["api.notifications_notificantion_list"] = notification_detect(app.view_functions["api.notifications_notificantion_list"])
    app.view_functions["api.challenges_challenge_attempt"] = challenge_attempt_decorator(app.view_functions["api.challenges_challenge_attempt"])
