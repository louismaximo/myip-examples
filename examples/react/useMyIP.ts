/**
 * useMyIP - React hook for fetching IP address and geolocation data
 *
 * @example
 * ```tsx
 * import { useMyIP } from './useMyIP';
 *
 * function MyComponent() {
 *   const { data, loading, error, refetch } = useMyIP();
 *
 *   if (loading) return <p>Loading...</p>;
 *   if (error) return <p>Error: {error}</p>;
 *
 *   return (
 *     <div>
 *       <p>IP: {data?.ip}</p>
 *       <p>Location: {data?.location.city}, {data?.location.country}</p>
 *       <button onClick={refetch}>Refresh</button>
 *     </div>
 *   );
 * }
 * ```
 */

import { useState, useEffect, useCallback } from 'react';

// Type definitions
interface Location {
  country: string;
  city: string;
  region: string;
  postalCode: string;
  timezone: string;
  latitude: string;
  longitude: string;
}

interface Network {
  asn: number;
  isp: string;
}

interface Cloudflare {
  colo: string;
  ray: string;
}

interface IPData {
  ip: string;
  type: 'IPv4' | 'IPv6';
  hostname?: string;
  connectionType?: 'residential' | 'vpn' | 'datacenter' | 'tor';
  location: Location;
  network: Network;
  cloudflare: Cloudflare;
}

interface DualStackData {
  ipv4: string | null;
  ipv6: string | null;
}

interface UseMyIPReturn {
  data: IPData | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

interface UseMyIPDualStackReturn {
  data: DualStackData | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

/**
 * Hook to fetch IP data from myip.foo API
 */
export function useMyIP(): UseMyIPReturn {
  const [data, setData] = useState<IPData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIP = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('https://myip.foo/api');

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result: IPData = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch IP data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIP();
  }, [fetchIP]);

  return { data, loading, error, refetch: fetchIP };
}

/**
 * Hook to fetch both IPv4 and IPv6 addresses
 * Uses dedicated endpoints that bypass Cloudflare's dual-stack routing
 */
export function useMyIPDualStack(): UseMyIPDualStackReturn {
  const [data, setData] = useState<DualStackData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDualStack = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // Fetch IPv4 and IPv6 in parallel
      const [ipv4Response, ipv6Response] = await Promise.allSettled([
        fetch('https://ipv4.myip.foo/ip', { signal: AbortSignal.timeout(5000) }),
        fetch('https://ipv6.myip.foo/ip', { signal: AbortSignal.timeout(5000) })
      ]);

      const ipv4 = ipv4Response.status === 'fulfilled' && ipv4Response.value.ok
        ? (await ipv4Response.value.text()).trim()
        : null;

      const ipv6 = ipv6Response.status === 'fulfilled' && ipv6Response.value.ok
        ? (await ipv6Response.value.text()).trim()
        : null;

      setData({ ipv4, ipv6 });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch dual-stack data');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDualStack();
  }, [fetchDualStack]);

  return { data, loading, error, refetch: fetchDualStack };
}

/**
 * Hook to get plain text IP only
 */
export function useMyIPPlain(): { ip: string | null; loading: boolean; error: string | null; refetch: () => void } {
  const [ip, setIP] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchIP = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('https://myip.foo/plain');

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.text();
      setIP(result.trim());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch IP');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIP();
  }, [fetchIP]);

  return { ip, loading, error, refetch: fetchIP };
}

export default useMyIP;
