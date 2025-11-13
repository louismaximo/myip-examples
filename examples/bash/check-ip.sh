#!/bin/bash
# check-ip.sh - Monitor IP changes and send notifications
# Usage: ./check-ip.sh

IP_FILE="/tmp/current_ip.txt"
CURRENT_IP=$(curl -s https://myip.foo/plain)

# Check if IP file exists
if [ -f "$IP_FILE" ]; then
  OLD_IP=$(cat "$IP_FILE")

  # Compare old and new IP
  if [ "$OLD_IP" != "$CURRENT_IP" ]; then
    echo "⚠️  IP changed: $OLD_IP → $CURRENT_IP"

    # Send notification (uncomment and configure)
    # curl -X POST https://your-webhook-url.com \
    #   -H "Content-Type: application/json" \
    #   -d "{\"message\": \"IP changed from $OLD_IP to $CURRENT_IP\"}"

    # Log to syslog
    logger "IP address changed from $OLD_IP to $CURRENT_IP"
  else
    echo "✅ IP unchanged: $CURRENT_IP"
  fi
else
  echo "📝 First run - storing current IP: $CURRENT_IP"
fi

# Save current IP
echo "$CURRENT_IP" > "$IP_FILE"
