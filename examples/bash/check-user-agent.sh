#!/bin/bash
# check-user-agent.sh - Display your browser's User-Agent string
# Usage: ./check-user-agent.sh

echo "🌐 Your User-Agent string:"
echo ""

USER_AGENT=$(curl -s https://myip.foo/user-agent)
echo "$USER_AGENT"

echo ""
echo "💡 Tip: Use this to verify User-Agent spoofing/masking"
