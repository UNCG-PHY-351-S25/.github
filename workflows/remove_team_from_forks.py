import os
import requests

ORG_NAME = "UNCG-PHY-351-S25"
TEAM_NAME = "Students"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

def get_team_id():
    url = f"https://api.github.com/orgs/{ORG_NAME}/teams"
    response = requests.get(url, headers=headers).json()
    for team in response:
        if team["name"] == TEAM_NAME:
            return team["id"]
    return None

def get_repos():
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos"
    response = requests.get(url, headers=headers).json()
    return response

def remove_team_access(repo_name, team_id):
    url = f"https://api.github.com/teams/{team_id}/repos/{ORG_NAME}/{repo_name}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Removed {TEAM_NAME} from {repo_name}")
    else:
        print(f"Failed to remove {TEAM_NAME} from {repo_name}: {response.text}")

def main():
    team_id = get_team_id()
    if not team_id:
        print("Team not found")
        return

    repos = get_repos()
    for repo in repos:
        if repo["fork"] and repo["name"] not in ["A-01", "A-02", "A-03", "A-04", "A-05", "A-06"]:  # Add your main repo names
            remove_team_access(repo["name"], team_id)

if __name__ == "__main__":
    main()
