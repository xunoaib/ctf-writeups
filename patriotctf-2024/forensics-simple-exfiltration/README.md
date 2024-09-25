# Simple Exfiltration

## Description

We've got some reports about information being sent out of our network. Can you figure out what message was sent out.

Author: Ryan Wong (shadowbringer007)

## Files

* [exfiltration_activity_pctf_challenge.pcapng](exfiltration_activity_pctf_challenge.pcapng)

## Solution

The packet capture contains many ICMP requests, each having suspiciously different TTLs in the 95 to 125 range. Decoding these as ASCII reveals the flag!

```bash
tshark -r exfiltration_activity_pctf_challenge.pcapng -Y "icmp.type == 8" -T fields -e ip.ttl  | awk '{ printf "%c", $1 }'
```

## Flag

`pctf{time_to_live_exfiltration}`
