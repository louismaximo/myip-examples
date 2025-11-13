#!/usr/bin/env node
/**
 * ip-lookup.js - Get IP address and location info
 * Usage: node ip-lookup.js
 */

async function getIPInfo() {
  try {
    // Fetch IP data from API
    const response = await fetch('https://myip.foo/api');

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Display results
    console.log('🌐 IP Information:');
    console.log('─────────────────────────────');
    console.log(`IP Address: ${data.ip} (${data.type})`);
    console.log(`\n📍 Location:`);
    console.log(`  Country: ${data.location.country}`);
    console.log(`  City: ${data.location.city}`);
    console.log(`  Region: ${data.location.region}`);
    console.log(`  Timezone: ${data.location.timezone}`);
    console.log(`  Coordinates: ${data.location.latitude}, ${data.location.longitude}`);
    console.log(`\n🌐 Network:`);
    console.log(`  ISP: ${data.network.isp}`);
    console.log(`  ASN: ${data.network.asn}`);
    console.log(`\n☁️  Cloudflare:`);
    console.log(`  Datacenter: ${data.cloudflare.colo}`);
    console.log(`  Ray ID: ${data.cloudflare.ray}`);

  } catch (error) {
    console.error('❌ Error fetching IP info:', error.message);
    process.exit(1);
  }
}

// Run the function
getIPInfo();
