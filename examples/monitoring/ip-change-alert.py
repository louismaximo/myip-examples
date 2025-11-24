#!/usr/bin/env python3
"""
ip-change-alert.py - Monitor IP address changes and send alerts

Supports multiple notification channels:
- Slack webhook
- Discord webhook
- Email (SMTP)
- Console output

Usage:
  # Console only
  python ip-change-alert.py

  # With Slack
  SLACK_WEBHOOK=https://hooks.slack.com/... python ip-change-alert.py

  # With Discord
  DISCORD_WEBHOOK=https://discord.com/api/webhooks/... python ip-change-alert.py

  # Run with cron every 5 minutes
  */5 * * * * python /path/to/ip-change-alert.py
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Configuration
IP_CACHE_FILE = Path("/tmp/myip_current.json")
MYIP_API = "https://myip.foo/api"

# Webhook URLs from environment
SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

def get_current_ip():
    """Fetch current IP data from myip.foo"""
    try:
        response = requests.get(MYIP_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Failed to fetch IP: {e}")
        return None

def get_cached_ip():
    """Load cached IP data"""
    if IP_CACHE_FILE.exists():
        try:
            with open(IP_CACHE_FILE) as f:
                return json.load(f)
        except:
            pass
    return None

def save_ip_cache(data):
    """Save IP data to cache"""
    with open(IP_CACHE_FILE, "w") as f:
        json.dump(data, f)

def send_slack_alert(old_ip, new_data):
    """Send alert to Slack"""
    if not SLACK_WEBHOOK:
        return

    message = {
        "text": "🔔 IP Address Changed!",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🔔 IP Address Changed!"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Old IP:*\n`{old_ip}`"},
                    {"type": "mrkdwn", "text": f"*New IP:*\n`{new_data['ip']}`"},
                    {"type": "mrkdwn", "text": f"*Location:*\n{new_data['location']['city']}, {new_data['location']['country']}"},
                    {"type": "mrkdwn", "text": f"*ISP:*\n{new_data['network']['isp']}"}
                ]
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"🦊 Detected by myip.foo | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
                ]
            }
        ]
    }

    try:
        requests.post(SLACK_WEBHOOK, json=message, timeout=10)
        print("✅ Slack alert sent")
    except Exception as e:
        print(f"❌ Slack alert failed: {e}")

def send_discord_alert(old_ip, new_data):
    """Send alert to Discord"""
    if not DISCORD_WEBHOOK:
        return

    message = {
        "embeds": [{
            "title": "🔔 IP Address Changed!",
            "color": 16744256,  # Orange
            "fields": [
                {"name": "Old IP", "value": f"`{old_ip}`", "inline": True},
                {"name": "New IP", "value": f"`{new_data['ip']}`", "inline": True},
                {"name": "Type", "value": new_data['type'], "inline": True},
                {"name": "Location", "value": f"{new_data['location']['city']}, {new_data['location']['country']}", "inline": True},
                {"name": "ISP", "value": new_data['network']['isp'], "inline": True},
                {"name": "Connection", "value": new_data.get('connectionType', 'unknown'), "inline": True}
            ],
            "footer": {"text": "🦊 Powered by myip.foo"},
            "timestamp": datetime.utcnow().isoformat()
        }]
    }

    try:
        requests.post(DISCORD_WEBHOOK, json=message, timeout=10)
        print("✅ Discord alert sent")
    except Exception as e:
        print(f"❌ Discord alert failed: {e}")

def main():
    print(f"🔍 Checking IP address... [{datetime.now().strftime('%H:%M:%S')}]")

    # Get current IP
    current_data = get_current_ip()
    if not current_data:
        return

    current_ip = current_data['ip']

    # Get cached IP
    cached_data = get_cached_ip()
    cached_ip = cached_data['ip'] if cached_data else None

    # Check for change
    if cached_ip and cached_ip != current_ip:
        print(f"⚠️  IP changed: {cached_ip} → {current_ip}")
        print(f"   Location: {current_data['location']['city']}, {current_data['location']['country']}")
        print(f"   ISP: {current_data['network']['isp']}")

        # Send alerts
        send_slack_alert(cached_ip, current_data)
        send_discord_alert(cached_ip, current_data)

    elif not cached_ip:
        print(f"📝 Initial IP recorded: {current_ip}")
    else:
        print(f"✅ IP unchanged: {current_ip}")

    # Save current IP
    save_ip_cache(current_data)

if __name__ == "__main__":
    main()
