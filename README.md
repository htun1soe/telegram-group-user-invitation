# Telegram Group Invite Tool

A small Python script that creates individual Telegram group invite links and sends them to opted-in recipients using Telethon.

## Requirements

- Python 3.10+
- Telegram API credentials from https://my.telegram.org
- Permission to create invite links in the target group

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file beside `main.py`:

   ```dotenv
   TELEGRAM_API_ID=YOUR_API_ID
   TELEGRAM_API_HASH=YOUR_API_HASH
   TELEGRAM_PHONE=YOUR_PHONE_NUMBER
   TELEGRAM_GROUP=@YourGroupUsername
   ```

3. Add opted-in recipients to `recipients.txt`, one username or phone number per line. Lines starting with `#` are ignored.

4. Run the script:

   ```bash
   python main.py
   ```

On the first run, Telegram may ask for a login code and your two-step verification password.

## Notes

- Your account must be able to access the group and create invite links.
- Phone numbers may not resolve unless the person is an accessible Telegram contact. Usernames can be used when available.
- Each invite link is limited to one successful join, but anyone who gets the link may use it.
- Send invitations only to people who agreed to receive them. Stop if Telegram applies a sending restriction.