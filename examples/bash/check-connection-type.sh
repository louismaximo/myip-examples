#!/bin/bash
# check-connection-type.sh - Detect if your connection is VPN/datacenter/residential
# Usage: ./check-connection-type.sh

echo "🔍 Checking connection type..."
echo ""

DATA=$(curl -s https://myip.foo/api/connection-type)

IP=$(echo "$DATA" | jq -r '.ip')
TYPE=$(echo "$DATA" | jq -r '.connectionType')
PROVIDER=$(echo "$DATA" | jq -r '.provider')
ASN=$(echo "$DATA" | jq -r '.asn')

echo "IP:              $IP"
echo "Connection Type: $TYPE"
echo "Provider:        $PROVIDER"
echo "ASN:             $ASN"

echo ""

# Color-coded status
case "$TYPE" in
  "residential")
    echo "✅ Residential connection (likely home/mobile ISP)"
    ;;
  "datacenter")
    echo "⚠️  Datacenter connection (hosting provider/VPS)"
    ;;
  "vpn")
    echo "🔒 VPN/Proxy detected"
    ;;
  *)
    echo "❓ Connection type unknown"
    ;;
esac
