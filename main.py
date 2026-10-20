
"""
Telegram Group Invite Tool
--------------------------
Create individual group invite links and send them to opted-in recipients.

Requirements:
    pip install -r requirements.txt

Before running:
    1. Configure your .env file.
    2. Add consenting Telegram contacts/usernames to recipients.txt.
    3. Make sure your account has permission to create group invite links.
"""

import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    PeerFloodError,
    UserPrivacyRestrictedError,
)

# Load private configuration from .env.
load_dotenv()

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
PHONE_NUMBER = os.environ["TELEGRAM_PHONE"]

# Use a public group username or a group ID you can access.
# For a private group, see the setup notes below.
GROUP = os.environ["TELEGRAM_GROUP"]

SESSION_NAME = "telegram_invite_session"
RECIPIENTS_FILE = Path("recipients.txt")


def load_recipients():
    """Read one opted-in Telegram username or phone number per line."""
    if not RECIPIENTS_FILE.exists():
        raise FileNotFoundError(
            "recipients.txt is missing. Create it and add opted-in recipients."
        )

    recipients = []

    for line in RECIPIENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Ignore blank lines and comments.
        if line and not line.startswith("#"):
            recipients.append(line)

    return recipients


async def generate_and_send_links():
    recipients = load_recipients()

    if not recipients:
        print("No recipients found. Nothing to do.")
        return

    # The session file stores authentication information.
    # Never share or publish this file.
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

    try:
        await client.start(phone=PHONE_NUMBER)
        print("Connected to Telegram.")

        # Resolve the group once. Your account must have access to it.
        group_entity = await client.get_entity(GROUP)

        for index, recipient in enumerate(recipients, start=1):
            print(
                f"\n[{index}/{len(recipients)}] "
                f"Processing {recipient}"
            )

            try:
                # This works when Telegram can resolve the recipient.
                # A phone number may need to be in your Telegram contacts.
                user = await client.get_input_entity(recipient)

                # Create a distinct invite link.
                # usage_limit=1 means one successful join via this link.
                invite = await client(
                    __import__(
                        "telethon.tl.functions.messages",
                        fromlist=["ExportChatInviteRequest"],
                    ).ExportChatInviteRequest(
                        peer=group_entity,
                        usage_limit=1,
                        title=f"Club invitation {index}",
                    )
                )

                message = (
                    "Hello! Here is your invitation to join "
                    "the Science and Tech Club.\n\n"
                    f"{invite.link}\n\n"
                    "Please let the organizer know if you have any trouble joining."
                )

                await client.send_message(user, message)
                print("Invitation sent successfully.")

            except UserPrivacyRestrictedError:
                print("Skipped: recipient privacy settings prevent messaging.")

            except ValueError:
                print(
                    "Skipped: Telegram could not resolve this recipient. "
                    "Try a valid username or an accessible contact."
                )

            except PeerFloodError:
                print(
                    "Telegram reported a sending restriction. "
                    "Stopping; do not retry to bypass the restriction."
                )
                break

            except FloodWaitError as error:
                print(
                    f"Telegram requires a wait of {error.seconds} seconds. "
                    "Stopping safely; run again only when appropriate."
                )
                break

            except Exception as error:
                print(f"Failed for this recipient: {error}")

    finally:
        await client.disconnect()
        print("\nDisconnected from Telegram.")


if __name__ == "__main__":
    asyncio.run(generate_and_send_links())
