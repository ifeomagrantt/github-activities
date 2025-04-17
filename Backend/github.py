import argparse, requests

parser = argparse.ArgumentParser(description="Github API Request")
parser.add_argument('username', type=str, help='github username')
parser.add_argument('--github-activity', action='store_true', help='get github recent activity')
args = parser.parse_args()

def github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch data.")
        return

    events = response.json()
    for event in events:
        type = event["type"]
        repo = event["repo"]["name"]

        if type == "PushEvent":
            commit_count = len(event["payload"]["commits"])
            print(f"- Pushed {commit_count} commit(s) to {repo}")
        elif type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"- {action.capitalize()} an issue in {repo}")
        elif type == "WatchEvent":
            print(f"- Starred {repo}")
        else:
            print(f"- {type.replace('Event', '')} in {repo}")

if args.github_activity:
    github_activity(username=args.username)
