# Impersonate

## Description

One may not be the one they claim to be.

http://chal.competitivecyber.club:9999/

Author: `_jungbahadurrana`

## Files

* [app.py](app.py)

## Solution

* [solve.py](solve.py)

The goal is to retrieve the flag from the `/admin` endpoint by impersonating the administrator with a forged session cookie. The server [cryptographically signs](https://en.wikipedia.org/wiki/Digital_signature) session cookies using `app.secret_key`, preventing client-side tampering of session data. If we can somehow leak the secret key, we can use it to sign our own session data, allowing the server to trust it as authentic.

In this challenge, the secret key is derived from the server start time, which is unknown at first. However, the `/status` page reveals the information needed to calculate it. From there, we can replicate the secret key on our end and use it to sign arbitrary session data.

#### Enumerating Available Endpoints
- **`/` (GET, POST):** Allows login with any username and password. The session includes a UUID based on the username and a secret.
- **`/user/<uid>` (GET):** Displays a message for guests.
- **`/admin` (GET):** Displays the flag if the session's `username` is "administrator" and `is_admin` is `True`.
- **`/status` (GET):** Provides the server's uptime and current time, indirectly leaking the start time needed to calculate the secret key.

#### Administrator Checks
To pass the administrator check, the following conditions must be met:
- `username` must be "administrator."
- Session must contain `is_admin = True`.
- Session cookie must be signed with `app.secret_key` to be valid.

#### Solution Steps
1. **Calculate the Secret Key:**
   - Visit `/status` to retrieve the server's uptime and current time. Calculate the server's start time using this information.
   - Derive the `app.secret_key` by hashing the start time with the fixed string "secret_key_<start_time>."

2. **Craft the Cookie:**
   - Forge a session dictionary containing:
     - `"is_admin": True`
     - `"username": "administrator"`
     - A valid UUID based on the username "administrator" and a not-so-secret UUID (`31333337-1337-1337-1337-133713371337`).
   - Sign the session cookie with the derived `app.secret_key` using a tool like [flask_unsign](https://github.com/Paradoxis/Flask-Unsign).

3. **Access Admin Page:**
   - Send the forged session cookie to `/admin` to access the flag: `PCTF{Imp3rs0n4t10n_Iz_Sup3r_Ezz}`.
