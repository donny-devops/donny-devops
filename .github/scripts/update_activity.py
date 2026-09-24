#!/usr/bin/env python3
"""
update_activity.py
Fetches recent public GitHub activity for donny-devops and updates README.md
between <!-- RECENT_ACTIVITY:START --> and <!-- RECENT_ACTIVITY:END --> tags.
"""

import json
import os
import re
import sys
import urllib.request

USERNAME = "donny-devops"
MAX_ITEMS = 6
README_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "README.md")
START_TAG = "<!-- RECENT_ACTIVITY:START -->"
END_TAG = "<!-- RECENT_ACTIVITY:END -->"


def fetch_events(username: str):
    url = f"https://api.github.com/users/{username}/events/public"
    headers = {
        "User-Agent": "Profile-Activity-Updater",
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching events: {e}", file=sys.stderr)
        return []
    return []


def format_events(events):
    lines = []
    seen = set()

    for ev in events:
        etype = ev.get("type")
        repo = ev.get("repo", {}).get("name")
        payload = ev.get("payload", {})
        created = ev.get("created_at", "")
        date_str = created[:10] if created else ""

        if not repo:
            continue

        repo_url = f"https://github.com/{repo}"
        repo_name = repo.split("/")[-1]

        msg = None
        if etype == "PushEvent":
            ref = payload.get("ref", "")
            branch = ref.replace("refs/heads/", "") if ref else "main"
            key = ("PushEvent", repo, branch, date_str)
            if key not in seen:
                seen.add(key)
                msg = f"- 🚀 **Pushed commits** to `{branch}` in [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        elif etype == "PullRequestEvent":
            action = payload.get("action", "")
            pr = payload.get("pull_request", {})
            pr_num = pr.get("number")
            pr_url = f"{repo_url}/pull/{pr_num}" if pr_num else repo_url
            verb = "Merged" if action in ("merged", "closed") and pr.get("merged", action == "merged") else action.capitalize()
            icon = "🟣" if verb == "Merged" else "🟢"
            key = ("PullRequestEvent", repo, pr_num, verb)
            if key not in seen:
                seen.add(key)
                num_text = f" #{pr_num}" if pr_num else ""
                msg = f"- {icon} **{verb} PR**{num_text} in [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        elif etype == "IssueCommentEvent":
            issue = payload.get("issue", {})
            issue_num = issue.get("number")
            issue_url = f"{repo_url}/issues/{issue_num}" if issue_num else repo_url
            key = ("IssueCommentEvent", repo, issue_num, date_str)
            if key not in seen:
                seen.add(key)
                num_text = f" #{issue_num}" if issue_num else ""
                msg = f"- 💬 **Commented on issue**{num_text} in [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        elif etype == "ReleaseEvent":
            rel = payload.get("release", {})
            tag = rel.get("tag_name", "")
            rel_url = rel.get("html_url", repo_url)
            key = ("ReleaseEvent", repo, tag)
            if key not in seen:
                seen.add(key)
                msg = f"- 🏷️ **Released** [`{tag}`]({rel_url}) in [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        elif etype == "CreateEvent":
            ref_type = payload.get("ref_type")
            ref = payload.get("ref")
            if ref_type == "repository":
                key = ("CreateEvent_repo", repo)
                if key not in seen:
                    seen.add(key)
                    msg = f"- 📦 **Created repository** [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"
            elif ref_type in ("branch", "tag") and ref:
                key = ("CreateEvent_ref", repo, ref)
                if key not in seen:
                    seen.add(key)
                    msg = f"- 🌱 **Created {ref_type}** `{ref}` in [`{repo_name}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        elif etype == "WatchEvent":
            key = ("WatchEvent", repo)
            if key not in seen:
                seen.add(key)
                msg = f"- ⭐ **Starred repository** [`{repo}`]({repo_url}) &nbsp;·&nbsp; *`{date_str}`*"

        if msg:
            lines.append(msg)
        if len(lines) >= MAX_ITEMS:
            break

    if not lines:
        return "- *No recent public activity to display.*"
    return "\n".join(lines)


def update_readme():
    readme_path = os.path.abspath(README_PATH)
    if not os.path.exists(readme_path):
        print(f"README not found at {readme_path}", file=sys.stderr)
        sys.exit(1)

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        f"{re.escape(START_TAG)}.*?{re.escape(END_TAG)}",
        re.DOTALL,
    )

    if not pattern.search(content):
        print(f"Activity markers not found in {readme_path}", file=sys.stderr)
        return False

    events = fetch_events(USERNAME)
    if not events:
        print("No events retrieved from GitHub API.")
        return False

    formatted = format_events(events)
    replacement = f"{START_TAG}\n{formatted}\n{END_TAG}"
    new_content = pattern.sub(replacement, content)

    if new_content != content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README.md updated with recent activity.")
        return True
    else:
        print("README.md already up to date.")
        return False


if __name__ == "__main__":
    update_readme()
