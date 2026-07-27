#!/usr/bin/env python3
"""
Read-only Microsoft 365 mail/calendar client for Claude Code.

Hard read-only by construction: the token it requests carries only
Mail.Read / Calendars.Read / User.Read. There is no send/draft/delete
code path, and even if there were, Graph would reject it with 403.

Setup (one time):
  1. Create an Entra app registration (see instructions), note the client id.
  2. export M365_CLIENT_ID="<your-app-client-id>"
  3. pip3 install msal requests
  4. python3 m365_read_only.py device-auth      # sign in once in the browser
  5. python3 m365_read_only.py whoami

Usage:
  python3 m365_read_only.py mail-list [--count 25] [--unread] [--folder inbox]
  python3 m365_read_only.py mail-read <message_id>
  python3 m365_read_only.py mail-search "<query>" [--count 25]
  python3 m365_read_only.py folders
  python3 m365_read_only.py cal-list [--days 7] [--count 50]
"""

import argparse
import json
import os
import sys

import msal
import requests

# Delegated, read-only. Never add Mail.Send / Mail.ReadWrite here.
SCOPES = [
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Calendars.Read",
    "https://graph.microsoft.com/User.Read",
]
GRAPH = "https://graph.microsoft.com/v1.0"

CLIENT_ID = os.environ.get("M365_CLIENT_ID", "")
# "common" works for both work/school and personal accounts.
AUTHORITY = f"https://login.microsoftonline.com/{os.environ.get('M365_TENANT_ID', 'common')}"
CACHE_PATH = os.path.expanduser("~/.config/m365-readonly/token_cache.json")


def _app():
    if not CLIENT_ID:
        sys.exit("Error: set M365_CLIENT_ID to your app registration's client id.")
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        cache.deserialize(open(CACHE_PATH).read())
    return msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache), cache


def _save(cache):
    if cache.has_state_changed:
        with open(CACHE_PATH, "w") as f:
            f.write(cache.serialize())
        os.chmod(CACHE_PATH, 0o600)


def device_auth():
    app, cache = _app()
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        sys.exit(f"Device flow failed: {flow}")
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)
    _save(cache)
    if "access_token" not in result:
        sys.exit(f"Auth failed: {result.get('error_description', result)}")
    print("Signed in. Scopes granted:", result.get("scope"))


def token():
    app, cache = _app()
    accounts = app.get_accounts()
    if not accounts:
        sys.exit("No cached account. Run: python3 m365_read_only.py device-auth")
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    _save(cache)
    if not result or "access_token" not in result:
        sys.exit("Token refresh failed. Re-run device-auth.")
    return result["access_token"]


def get(endpoint, params=None):
    r = requests.get(f"{GRAPH}{endpoint}",
                     headers={"Authorization": f"Bearer {token()}"},
                     params=params, timeout=30)
    if r.status_code >= 400:
        sys.exit(f"Graph error {r.status_code}: {r.text[:500]}")
    return r.json()


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("device-auth")
    sub.add_parser("whoami")
    sub.add_parser("folders")
    m = sub.add_parser("mail-list")
    m.add_argument("--count", type=int, default=25)
    m.add_argument("--unread", action="store_true")
    m.add_argument("--folder", default="inbox")
    r = sub.add_parser("mail-read")
    r.add_argument("message_id")
    s = sub.add_parser("mail-search")
    s.add_argument("query")
    s.add_argument("--count", type=int, default=25)
    c = sub.add_parser("cal-list")
    c.add_argument("--days", type=int, default=7)
    c.add_argument("--count", type=int, default=50)
    a = p.parse_args()

    if a.cmd == "device-auth":
        return device_auth()

    if a.cmd == "whoami":
        me = get("/me")
        print(json.dumps({k: me.get(k) for k in
                          ("displayName", "mail", "userPrincipalName")}, indent=2))

    elif a.cmd == "folders":
        for f in get("/me/mailFolders", {"$top": 100}).get("value", []):
            print(f"{f['displayName']:<35} unread={f.get('unreadItemCount', 0):<5} {f['id']}")

    elif a.cmd == "mail-list":
        params = {"$top": a.count, "$orderby": "receivedDateTime desc",
                  "$select": "id,subject,from,receivedDateTime,isRead,bodyPreview"}
        if a.unread:
            params["$filter"] = "isRead eq false"
        data = get(f"/me/mailFolders/{a.folder}/messages", params)
        for msg in data.get("value", []):
            sender = msg.get("from", {}).get("emailAddress", {})
            flag = " " if msg.get("isRead") else "*"
            print(f"{flag} [{msg['receivedDateTime']}] {sender.get('address', '?')}")
            print(f"  {msg.get('subject', '(no subject)')}")
            print(f"  {(msg.get('bodyPreview') or '')[:160]}")
            print(f"  id: {msg['id']}\n")

    elif a.cmd == "mail-read":
        msg = get(f"/me/messages/{a.message_id}")
        sender = msg.get("from", {}).get("emailAddress", {})
        print(f"From:    {sender.get('name')} <{sender.get('address')}>")
        print(f"To:      {', '.join(t['emailAddress']['address'] for t in msg.get('toRecipients', []))}")
        print(f"Date:    {msg.get('receivedDateTime')}")
        print(f"Subject: {msg.get('subject')}")
        atts = msg.get("hasAttachments")
        if atts:
            print("Attachments: yes")
        print("-" * 60)
        print(msg.get("body", {}).get("content", ""))

    elif a.cmd == "mail-search":
        data = get("/me/messages", {"$search": f'"{a.query}"', "$top": a.count})
        for msg in data.get("value", []):
            sender = msg.get("from", {}).get("emailAddress", {})
            print(f"[{msg.get('receivedDateTime')}] {sender.get('address', '?')}")
            print(f"  {msg.get('subject')}")
            print(f"  id: {msg['id']}\n")

    elif a.cmd == "cal-list":
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        data = get("/me/calendarView", {
            "startDateTime": now.isoformat(),
            "endDateTime": (now + timedelta(days=a.days)).isoformat(),
            "$top": a.count, "$orderby": "start/dateTime",
        })
        for ev in data.get("value", []):
            print(f"[{ev['start']['dateTime'][:16]}] {ev.get('subject')}")
            if ev.get("location", {}).get("displayName"):
                print(f"  @ {ev['location']['displayName']}")


if __name__ == "__main__":
    main()
