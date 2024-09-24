# giraffe notes

## Description

I bet you can't access my notes on giraffes!

http://chal.competitivecyber.club:8081

**Flag format: CACI{.*}**

Author: [CACI](https://www.caci.com)

## Files

* [index.php](index.php)

## Solution

In this challenge, the server determines access permissions based on client-provided information, specifically through the `X-Forwarded-For` HTTP header. Depending on whether the request is "allowed," the server will display one of two web pages: one containing the flag and another without it.

A request is considered "allowed" if it meets the following criteria:
- The `X-Forwarded-For` HTTP header must be defined.
- The value of this header must match one of the allowed IP addresses: `localhost` or `127.0.0.1`.

As a client, we can craft an HTTP request with the `X-Forwarded-For` header set to either `localhost` or `127.0.0.1`. This can be done using the following `curl` command:

```bash
curl http://chal.competitivecyber.club:8081 -H 'X-Forwarded-For: localhost'
```

Sending this request causes the server to display the web page with the flag.

Flag: `CACI{1_lik3_g1raff3s_4_l0t}``
