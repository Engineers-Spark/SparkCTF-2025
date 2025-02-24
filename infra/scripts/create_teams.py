import csv
import requests

TEAM_URL = "http://localhost/api/v1/teams"
USER_URL = "http://localhost/api/v1/users"

HEADERS = {"Authorization": "Token REDACTED"}

CSV_FILE = "accounts.csv"

def create_accounts(csv_file):
    with open(csv_file, newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['Username'].strip()
            password = row['Password'].strip()
            
            # Create team
            team_data = {
                "name": username,
                "password": password,
                "hidden": False,
                "banned": False,
                "fields": []
            }
            team_response = requests.post(TEAM_URL, json=team_data, headers=HEADERS)
            print(f"Team Response for {username}: {team_response.status_code}, {team_response.text}")
            
            # Create user
            user_data = {
                "name": username,
                "email": f"{username}@example.com",
                "password": password,
                "type": "user",
                "verified": False,
                "hidden": False,
                "banned": False,
                "fields": []
            }
            user_response = requests.post(USER_URL, json=user_data, headers=HEADERS)
            print(f"User Response for {username}: {user_response.status_code}, {user_response.text}")

if __name__ == "__main__":
    create_accounts(CSV_FILE)
