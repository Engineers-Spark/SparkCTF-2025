import requests, time, socket, logging
from discord_webhook import DiscordWebhook, DiscordEmbed
from schedule import every, repeat, run_pending

logging.basicConfig(filename="./jobs.log",level=logging.DEBUG)

DISCORD_WEBHOOK = "REDACTED"
HTTP_CHALLENGES = {
                    "todo": [1, "https://todo.espark.tn"],
                    "bugreportgen": [1, "https://bugreportgen.espark.tn"],
                    "capitalism": [1, "https://capitalism.espark.tn"],
                    "grades": [1, "https://grades.espark.tn"],
                    "puzzle-solving":[1,"https://puzzle-solving.espark.tn"],
                    "Permutation Paradox":[1,"https://permutation-paradox.espark.tn"]
                }
TCP_CHALLENGES = {
                    "Hash Overdrive": [1, "tcp.espark.tn:5778"],
                    "Echo Chamber": [1, "tcp.espark.tn:6322"],
                    "Guess The Flag": [1, "tcp.espark.tn:6543"],
                    "roller": [1, "tcp.espark.tn:5322"],
                    "www": [1, "tcp.espark.tn:5515"],
                    "retro": [1, "tcp.espark.tn:6112"],
                }

OTHER = {
    "CTFd": [1, "https://ctf.espark.tn"],
    "LIVESCOREBOARD": [1, "https://live-score.espark.tn"],
}


@repeat(every(30).minutes, HTTP_CHALLENGES)
def web_check(HTTP_CHALLENGES):
     for challenge in HTTP_CHALLENGES:
        service = HTTP_CHALLENGES[challenge]
        try:
            r = requests.get(service[1])
            r.raise_for_status()
            # if it was already down then send message saying its up
            if not service[0]:
                send_discord("DOWNTIME ALERT ✅",challenge,"UP")

            service[0] = 1
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if service[0]:
                service[0] = 0
                send_discord("DOWNTIME ALERT⚠️",challenge,"DOWN")
                logging.info(f"SERVICE: {challenge}\nSTATUS: DOWN\n")


@repeat(every(30).minutes, TCP_CHALLENGES)
def pwn_check(TCP_CHALLENGES):
    for challenge in TCP_CHALLENGES:
        service = TCP_CHALLENGES[challenge]
        try:
            host, port = service[1].split(':')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            port = int(port)
            s.connect((host, port))
            if not service[0]:
                send_discord("DOWNTIME ALERT ✅",challenge,"UP")
            service[0] = 1
        except:
            # if status already down don't send message
            if service[0]:
                service[0] = 0
                send_discord("DOWNTIME ALERT⚠️",challenge,"DOWN")
                logging.info(f"SERVICE: {challenge}\nSTATUS: DOWN\n")


@repeat(every(30).minutes, OTHER)
def other(OTHER):
    for link in OTHER:
        service = OTHER[link]
        try:
            r = requests.get(service[1])
            r.raise_for_status()
            if not service[0]:
                send_discord("DOWNTIME ALERT ✅",link,"UP")
            service[0] = 1
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # if status already down don't send message
            if service[0]:
                service[0] = 0
                send_discord("DOWNTIME ALERT⚠️",link,"DOWN")
                logging.info(f"SERVICE: {link}\nSTATUS: DOWN\n")

def send_discord(title,service,status):
    webhook = DiscordWebhook(DISCORD_WEBHOOK)
    embed = DiscordEmbed(title=title,description=f"<@&1186753492027707444> It appears that the service **{service}** is **{status}** !!")
    embed.set_timestamp()
    webhook.add_embed(embed)
    webhook.execute()

while True:
    run_pending()
    time.sleep(1)