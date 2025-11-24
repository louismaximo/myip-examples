#!/usr/bin/env python3
"""
dual-stack-check.py - Check both IPv4 and IPv6 addresses

Uses dedicated endpoints that bypass Cloudflare's dual-stack routing:
  - ipv4.myip.foo/ip - Returns IPv4 only (A record)
  - ipv6.myip.foo/ip - Returns IPv6 only (AAAA record)

Usage: python dual-stack-check.py
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_ipv4():
    """Check IPv4 connectivity"""
    try:
        response = requests.get('https://ipv4.myip.foo/ip', timeout=5)
        return ('IPv4', response.text.strip())
    except Exception as e:
        return ('IPv4', None)

def check_ipv6():
    """Check IPv6 connectivity"""
    try:
        response = requests.get('https://ipv6.myip.foo/ip', timeout=5)
        return ('IPv6', response.text.strip())
    except Exception as e:
        return ('IPv6', None)

def get_full_info():
    """Get full connection info from main API"""
    try:
        response = requests.get('https://myip.foo/api', timeout=5)
        return response.json()
    except Exception as e:
        return None

def main():
    print("🔍 Checking dual-stack connectivity...\n")

    # Check IPv4 and IPv6 in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(check_ipv4),
            executor.submit(check_ipv6)
        ]

        results = {}
        for future in as_completed(futures):
            ip_type, ip_address = future.result()
            results[ip_type] = ip_address

    # Display results
    print("📡 IPv4:")
    if results.get('IPv4'):
        print(f"   ✅ {results['IPv4']}")
    else:
        print("   ❌ No IPv4 connectivity")

    print("\n📡 IPv6:")
    if results.get('IPv6'):
        print(f"   ✅ {results['IPv6']}")
    else:
        print("   ❌ No IPv6 connectivity")

    # Get full info
    print("\n📊 Full connection info:")
    info = get_full_info()
    if info:
        print(f"   IP: {info['ip']}")
        print(f"   Type: {info['type']}")
        print(f"   Location: {info['location']['city']}, {info['location']['country']}")
        print(f"   ISP: {info['network']['isp']}")

        # Check connection type if available
        if 'connectionType' in info:
            conn_type = info['connectionType']
            if conn_type == 'residential':
                print(f"   Connection: 🏠 Residential")
            elif conn_type == 'vpn':
                print(f"   Connection: 🔒 VPN")
            elif conn_type == 'datacenter':
                print(f"   Connection: 🖥️ Datacenter")
            elif conn_type == 'tor':
                print(f"   Connection: 🧅 Tor")

    print("\n🦊 Powered by myip.foo")

if __name__ == "__main__":
    main()
