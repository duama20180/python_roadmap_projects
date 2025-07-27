# import requests
#
# BASE_URL = 'https://api.github.com/users/'
#
# def get_user_activity(user_name):
#     try:
#         response = requests.get(f"{BASE_URL}{user_name}/events")
#         response.raise_for_status()
#         data = response.json()
#         return data
#     except requests.exceptions.RequestException as e:
#         return e
#
#
# if __name__ == '__main__':
#     user_name = input(f"Enter an username: ")
#     print( get_user_activity(user_name))
#
#
#



import sys
import urllib.request
import urllib.error
import json
from datetime import datetime


def fetch_user_events(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        request = urllib.request.Request(url, headers={"User-Agent": "github-activity-cli"})
        with urllib.request.urlopen(request) as response:
            if response.getcode() == 200:
                return json.loads(response.read().decode())
            else:
                print(f"Error: Received status code {response.getcode()}")
                return None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        elif e.code == 403:
            print("Error: API rate limit exceeded. Please try again later.")
        else:
            print(f"HTTP Error: {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid response from GitHub API.")
        return None


def format_event(event):
    event_type = event["type"]
    repo_name = event["repo"]["name"]
    created_at = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")

    if event_type == "PushEvent":
        commit_count = len(event["payload"]["commits"])
        return f"Pushed {commit_count} commit{'s' if commit_count > 1 else ''} to {repo_name} at {created_at}"
    elif event_type == "IssuesEvent":
        action = event["payload"]["action"].capitalize()
        issue_title = event["payload"]["issue"]["title"]
        return f"{action} issue '{issue_title}' in {repo_name} at {created_at}"
    elif event_type == "WatchEvent":
        return f"Starred {repo_name} at {created_at}"
    elif event_type == "PullRequestEvent":
        action = event["payload"]["action"].capitalize()
        pr_title = event["payload"]["pull_request"]["title"]
        return f"{action} pull request '{pr_title}' in {repo_name} at {created_at}"
    elif event_type == "CreateEvent":
        ref_type = event["payload"]["ref_type"]
        ref = event["payload"]["ref"] if event["payload"]["ref"] else repo_name
        return f"Created {ref_type} '{ref}' in {repo_name} at {created_at}"
    else:
        return f"{event_type} in {repo_name} at {created_at}"


def main():

    username = input("Enter GitHub username: ")
    print(f"Fetching recent activity for {username}...")

    events = fetch_user_events(username)
    if not events:
        sys.exit(1)

    print(f"\nRecent activity for {username}:")
    print("-" * 50)
    for event in events[:10]:
        print(format_event(event))


if __name__ == "__main__":
    main()