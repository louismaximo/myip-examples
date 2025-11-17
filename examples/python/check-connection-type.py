#!/usr/bin/env python3
"""
check-connection-type.py - Detect if your connection is VPN/datacenter/residential
Usage: python3 check-connection-type.py
"""

import requests
import sys

def check_connection_type():
    """Check connection type using myip.foo API"""
    try:
        response = requests.get('https://myip.foo/api/connection-type', timeout=5)
        response.raise_for_status()
        data = response.json()

        ip = data.get('ip', 'Unknown')
        conn_type = data.get('connectionType', 'unknown')
        provider = data.get('provider', 'Unknown')
        asn = data.get('asn', 'Unknown')

        print(f"🔍 Connection Analysis:\n")
        print(f"IP:              {ip}")
        print(f"Connection Type: {conn_type}")
        print(f"Provider:        {provider}")
        print(f"ASN:             {asn}\n")

        # Status message
        if conn_type == 'residential':
            print("✅ Residential connection (likely home/mobile ISP)")
            return 0
        elif conn_type == 'datacenter':
            print("⚠️  Datacenter connection (hosting provider/VPS)")
            return 1
        elif conn_type == 'vpn':
            print("🔒 VPN/Proxy detected")
            return 2
        else:
            print("❓ Connection type unknown")
            return 3

    except requests.RequestException as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 99

if __name__ == '__main__':
    sys.exit(check_connection_type())
