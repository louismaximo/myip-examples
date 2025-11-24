#!/bin/bash
# dual-stack-check.sh - Check both IPv4 and IPv6 addresses
# Uses dedicated endpoints that bypass Cloudflare's dual-stack routing
#
# Endpoints:
#   ipv4.myip.foo/ip - Returns IPv4 only (A record)
#   ipv6.myip.foo/ip - Returns IPv6 only (AAAA record)
#
# Usage: ./dual-stack-check.sh

echo "🔍 Checking dual-stack connectivity..."
echo ""

# Check IPv4
echo "📡 IPv4:"
IPV4=$(curl -s --connect-timeout 5 https://ipv4.myip.foo/ip 2>/dev/null)
if [ -n "$IPV4" ]; then
    echo "   ✅ $IPV4"
else
    echo "   ❌ No IPv4 connectivity"
fi

echo ""

# Check IPv6
echo "📡 IPv6:"
IPV6=$(curl -s --connect-timeout 5 https://ipv6.myip.foo/ip 2>/dev/null)
if [ -n "$IPV6" ]; then
    echo "   ✅ $IPV6"
else
    echo "   ❌ No IPv6 connectivity"
fi

echo ""

# Get full info from main API
echo "📊 Full connection info:"
curl -s https://myip.foo/api | jq -r '"   IP: \(.ip)\n   Type: \(.type)\n   Location: \(.location.city), \(.location.country)\n   ISP: \(.network.isp)"'

echo ""
echo "🦊 Powered by myip.foo"
