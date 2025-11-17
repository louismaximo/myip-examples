#!/bin/bash
# check-headers.sh - Display all HTTP headers sent by your browser
# Usage: ./check-headers.sh

echo "🔍 Fetching HTTP headers from myip.foo..."
echo ""

curl -s https://myip.foo/headers | jq '.'

echo ""
echo "💡 Tip: Check for header leaks when using VPN/proxy"
