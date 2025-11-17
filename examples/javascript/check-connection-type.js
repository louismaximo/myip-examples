#!/usr/bin/env node
/**
 * check-connection-type.js - Detect if your connection is VPN/datacenter/residential
 * Usage: node check-connection-type.js
 */

async function checkConnectionType() {
  try {
    const response = await fetch('https://myip.foo/api/connection-type');

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    const { ip, connectionType, provider, asn } = data;

    console.log('🔍 Connection Analysis:\n');
    console.log(`IP:              ${ip || 'Unknown'}`);
    console.log(`Connection Type: ${connectionType || 'unknown'}`);
    console.log(`Provider:        ${provider || 'Unknown'}`);
    console.log(`ASN:             ${asn || 'Unknown'}\n`);

    // Status message
    switch (connectionType) {
      case 'residential':
        console.log('✅ Residential connection (likely home/mobile ISP)');
        process.exit(0);
        break;
      case 'datacenter':
        console.log('⚠️  Datacenter connection (hosting provider/VPS)');
        process.exit(1);
        break;
      case 'vpn':
        console.log('🔒 VPN/Proxy detected');
        process.exit(2);
        break;
      default:
        console.log('❓ Connection type unknown');
        process.exit(3);
    }
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(99);
  }
}

checkConnectionType();
