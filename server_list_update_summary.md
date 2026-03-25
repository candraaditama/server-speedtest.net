# Speedtest.net Server List Update Summary

**Date:** March 25, 2026

## What was done

All three MikroTik [.rsc](file:///d:/Aplikasi/Laragon/www/server-speedtest.net/US%20server-speedtest.net.rsc) server list files have been updated with the latest Speedtest.net (Ookla) server data, fetched directly from the live Ookla API (`https://www.speedtest.net/api/js/servers`).

## Updated Files

| File | Servers (Before) | Servers (After) | Change |
|------|:-:|:-:|:-:|
| `ASEAN server-speedtest.net.rsc` | ~1,001 | ~1,700 | +~699 |
| `EUROPE server-speedtest.net.rsc` | ~1,000 | ~2,048 | +~1,048 |
| `US server-speedtest.net.rsc` | ~1,000 | ~1,886 | +~886 |
| **Total** | **~3,001** | **~5,632** | **+~2,631** |

## How it works

A Python script ([fetch_servers.py](file:///d:/Aplikasi/Laragon/www/server-speedtest.net/fetch_servers.py)) was created to:

1. Query the Ookla Speedtest API from **300+ geographic coordinates** across all three regions
2. Extract unique server hostnames (removing port numbers and `.prod.hosts.ooklaserver.net` suffixes)
3. Classify servers into the correct region based on their country code
4. Sort servers by country → city → hostname
5. Write properly formatted MikroTik [.rsc](file:///d:/Aplikasi/Laragon/www/server-speedtest.net/US%20server-speedtest.net.rsc) files with CRLF line endings

### Region Classification

- **ASEAN**: Indonesia, Singapore, Malaysia, Thailand, Vietnam, Philippines, Cambodia, Myanmar, Laos, Brunei, Timor-Leste, Taiwan, Hong Kong, Macau, Australia, New Zealand, Pacific Islands, South Asia (India, Bangladesh, Sri Lanka, etc.), China, Japan, Korea, Mongolia
- **EUROPE**: All European countries, Nordics, Baltics, Eastern Europe, Russia, Turkey, Caucasus
- **US**: USA, Canada, Mexico, Central America, Caribbean, South America

## How to re-run in the future

To update the server list again in the future, simply run:

```bash
python fetch_servers.py
```

> [!NOTE]
> The script queries the API from 300+ locations with a 0.3s delay between requests. Total runtime is approximately **3-5 minutes**.

> [!IMPORTANT]
> The Ookla API returns servers based on proximity to the queried coordinates (up to 100 per query). While the script covers a wide range of coordinates, some servers in remote areas may not be captured.
