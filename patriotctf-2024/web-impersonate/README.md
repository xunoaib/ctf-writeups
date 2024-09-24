# Impersonate

## Description

One may not be the one they claim to be.

http://chal.competitivecyber.club:9999/

Author: `_jungbahadurrana`

## Files

* [app.py](app.py)

## Solution

* ⭐ [solve.py](solve.py) ⭐

The goal is to retrieve the flag from the `/admin` endpoint by forging a session cookie which impersonates the administrator.

When users log in, the server generates and signs a session cookie for them using a hidden `app.secret_key` which prevents them from tampering with session data. However, if we can obtain this key, we can craft and sign custom session data that the server will trust.

- The key is based on the server's start time, which can be calculated using data from the `/status` page (`start_time = current_time - uptime`).
- Once we derive the secret key, we can sign arbitrary session data.

I used [Flask Unsign](https://github.com/Paradoxis/Flask-Unsign) for this challenge. While I imported it as a library in my [solver script](solve.py), it also provides command-line tools.

#### Available Endpoints
- **`/` (GET, POST):** Logs in with any username/password.
- **`/user/<uid>` (GET):** Displays a guest message.
- **`/admin` (GET):** Displays the flag if `username = "administrator"` and `is_admin = True`.
- **`/status` (GET):** Leaks the server's start time.

#### Solution

1. **Derive Secret Key:**
   - Use the `/status` page to calculate the server’s start time.
   - Hash the start time with `"secret_key_<start_time>"` to obtain the `app.secret_key` (per the challenge code).

2. **Craft the Cookie:**
   - Create forged session data: `{"is_admin": True, "username": "administrator", "uid": "02ec19dc-bb01-5942-a640-7099cda78081"}`.
   - The administrator's UID is generated using `uuid.uuid5(secret, 'administrator')`. The `secret` is hardcoded in their source as `uuid.UUID('31333337-1337-1337-1337-133713371337')`.
   - Sign the session data using [Flask Unsign](https://github.com/Paradoxis/Flask-Unsign) with the derived `app.secret_key`.

3. **Access Flag:**
   - Send the signed cookie to `/admin` to retrieve the flag.

Flag: `PCTF{Imp3rs0n4t10n_Iz_Sup3r_Ezz}`
