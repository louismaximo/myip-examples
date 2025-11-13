#!/usr/bin/env python3
"""
vpn-checker.py - Verify VPN connection status
Usage: python3 vpn-checker.py [expected_country]
Example: python3 vpn-checker.py NL
"""

import requests
import sys

def verify_vpn(expected_country):
    """Check if VPN is connected to expected country"""
    try:
        # Fetch IP data
        response = requests.get('https://myip.foo/api', timeout=5)
        response.raise_for_status()
        data = response.json()

        # Extract location info
        ip = data['ip']
        actual_country = data['location']['country']
        city = data['location']['city']
        isp = data['network']['isp']

        # Check if country matches
        if actual_country == expected_country:
            print(f"✅ VPN connected to {expected_country}")
            print(f"   IP: {ip}")
            print(f"   Location: {city}, {actual_country}")
            print(f"   ISP: {isp}")
            return True
        else:
            print(f"❌ VPN not connected to {expected_country}")
            print(f"   Current location: {city}, {actual_country}")
            print(f"   IP: {ip}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Error checking VPN status: {e}")
        return False

if __name__ == "__main__":
    # Get expected country from command line or default to US
    expected = sys.argv[1] if len(sys.argv) > 1 else "US"

    # Verify VPN and exit with appropriate status code
    success = verify_vpn(expected)
    sys.exit(0 if success else 1)
