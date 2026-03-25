# Speedtest.net Server List

Speedtest.net (Ookla) server list in MikroTik RouterOS firewall address-list format.  
Useful for bypassing bandwidth limits or applying QoS rules specifically for speed test traffic.

## Server Files

| File | Region | Servers |
|------|--------|--------:|
| `ASEAN server-speedtest.net.rsc` | ASEAN, Asia-Pacific, Oceania, South Asia, East Asia | ~1,700 |
| `EUROPE server-speedtest.net.rsc` | Europe, Nordics, Baltics, Russia, Turkey, Caucasus | ~2,048 |
| `US server-speedtest.net.rsc` | USA, Canada, Mexico, Central America, Caribbean, South America | ~1,886 |
| **Total** | | **~5,632** |

> Last updated: **March 25, 2026**

## Usage

1. Upload the `.rsc` file(s) to your MikroTik router.
2. Open the terminal and run:

```
/import file="ASEAN server-speedtest.net.rsc"
```

3. The servers will be added to the `speedtest` address list under `/ip firewall address-list`.

## Updating the Server List

A Python script is included to fetch the latest servers directly from the Ookla Speedtest API.

```bash
python fetch_servers.py
```

The script queries the API from **300+ geographic coordinates** across all regions to build a comprehensive server list. It takes approximately 3–5 minutes to complete.

### Requirements

- Python 3.6+
- Internet connection (no additional packages required, uses only standard library)

## License

Feel free to use and update the list.
